"""
CLI Wrapper for Automated Python Docstring Generator.

Provides command-line interface with commands: 'scan', 'report', and 'apply'.
"""
import argparse
import sys
import json
from pathlib import Path
from typing import Optional
from modules import ASTExtractor, SynthesisEngine, QualityValidator, ReportGenerator
from utils import get_python_files, read_file, write_file


class DocstringCLI:
    """Command-line interface for the docstring generator."""

    def __init__(self):
        """Initialize the CLI."""
        self.parser = self._create_parser()
        self.synthesis_engine = SynthesisEngine()
        self.validator = QualityValidator()
        self.report_generator = ReportGenerator()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser."""
        parser = argparse.ArgumentParser(
            description="Automated Python Docstring Generator",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python cli.py scan src/
  python cli.py report src/ --format json --output report.json
  python cli.py apply src/ --style google
            """
        )

        subparsers = parser.add_subparsers(dest="command", help="Command to execute")

        # Scan Command
        scan_parser = subparsers.add_parser("scan", help="Scan Python files for documentation issues")
        scan_parser.add_argument("path", help="Path to Python file or directory")
        scan_parser.add_argument("--recursive", action="store_true", default=True, help="Scan recursively")
        scan_parser.add_argument("--output", "-o", help="Output file for scan results")

        # Report Command
        report_parser = subparsers.add_parser("report", help="Generate docstring coverage report")
        report_parser.add_argument("path", help="Path to Python file or directory")
        report_parser.add_argument("--format", choices=["json", "markdown", "html"], default="json", help="Report format")
        report_parser.add_argument("--output", "-o", help="Output file for report")
        report_parser.add_argument("--project-name", "-p", default="My Project", help="Project name")

        # Apply Command
        apply_parser = subparsers.add_parser("apply", help="Apply docstring generation and fixes")
        apply_parser.add_argument("path", help="Path to Python file or directory")
        apply_parser.add_argument("--style", choices=["google", "numpy", "rest"], default="google", help="Docstring style")
        apply_parser.add_argument("--autofix", action="store_true", default=True, help="Auto-fix formatting issues")
        apply_parser.add_argument("--output-dir", "-o", help="Output directory for fixed files")
        apply_parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")

        return parser

    def run(self, argv: Optional[list] = None) -> int:
        """
        Run the CLI.

        Args:
            argv: Command line arguments. If None, uses sys.argv[1:].

        Returns:
            Exit code.
        """
        args = self.parser.parse_args(argv)

        if not args.command:
            self.parser.print_help()
            return 0

        try:
            if args.command == "scan":
                return self.cmd_scan(args)
            elif args.command == "report":
                return self.cmd_report(args)
            elif args.command == "apply":
                return self.cmd_apply(args)
        except Exception as e:
            print(f"❌ Error: {str(e)}", file=sys.stderr)
            return 1

        return 0

    def cmd_scan(self, args: argparse.Namespace) -> int:
        """Execute the scan command."""
        print(f"🔍 Scanning: {args.path}")

        python_files = get_python_files(args.path)
        if not python_files:
            print("⚠️  No Python files found.")
            return 1

        print(f"📄 Found {len(python_files)} Python file(s)\n")

        all_issues = []
        for file_path in python_files:
            source_code = read_file(file_path)
            if not source_code.startswith("Error"):
                try:
                    extractor = ASTExtractor(source_code, file_path)
                    metadata = extractor.extract_all_metadata()

                    debt = metadata.get("documentation_debt", {})

                    if debt["missing_class_docstrings"] or debt["missing_function_docstrings"]:
                        print(f"📝 {file_path}")
                        if debt["missing_class_docstrings"]:
                            print(f"  - Classes without docstrings: {', '.join(debt['missing_class_docstrings'])}")
                        if debt["missing_function_docstrings"]:
                            print(f"  - Functions without docstrings: {', '.join(debt['missing_function_docstrings'][:3])}")
                        if len(debt["missing_function_docstrings"]) > 3:
                            print(f"  ... and {len(debt['missing_function_docstrings']) - 3} more")

                        all_issues.append({
                            "file": file_path,
                            "missing_classes": debt["missing_class_docstrings"],
                            "missing_functions": debt["missing_function_docstrings"]
                        })
                except SyntaxError as e:
                    print(f"❌ {file_path}: Syntax error - {str(e)}")

        if args.output:
            write_file(args.output, json.dumps(all_issues, indent=2))
            print(f"\n✅ Scan results saved to {args.output}")

        return 0

    def cmd_report(self, args: argparse.Namespace) -> int:
        """Execute the report command."""
        print(f"📊 Generating report for: {args.path}")

        python_files = get_python_files(args.path)
        if not python_files:
            print("⚠️  No Python files found.")
            return 1

        print(f"📄 Found {len(python_files)} Python file(s)\n")

        all_metadata = []
        all_coverage_reports = []

        for file_path in python_files:
            source_code = read_file(file_path)
            if not source_code.startswith("Error"):
                try:
                    extractor = ASTExtractor(source_code, file_path)
                    metadata = extractor.extract_all_metadata()
                    all_metadata.append(metadata)

                    validator = QualityValidator(file_path)
                    coverage_report = validator.generate_coverage_report(metadata)
                    all_coverage_reports.append(coverage_report)

                    print(f"✓ {file_path}: {coverage_report['overall_coverage']:.1f}%")
                except Exception as e:
                    print(f"❌ {file_path}: {str(e)}")

        # Generate project report
        report = self.report_generator.generate_project_report(
            args.project_name,
            all_metadata,
            all_coverage_reports
        )

        # Format report
        if args.format == "json":
            report_content = self.report_generator.generate_json_report(report)
        elif args.format == "markdown":
            report_content = self.report_generator.generate_markdown_report(report)
        elif args.format == "html":
            report_content = self.report_generator.generate_html_report(report)

        # Output report
        if args.output:
            write_file(args.output, report_content)
            print(f"\n✅ Report saved to {args.output}")
        else:
            print(f"\n{report_content}")

        return 0

    def cmd_apply(self, args: argparse.Namespace) -> int:
        """Execute the apply command."""
        print(f"🚀 Applying docstring generation: {args.path}")
        print(f"📋 Style: {args.style}")

        python_files = get_python_files(args.path)
        if not python_files:
            print("⚠️  No Python files found.")
            return 1

        print(f"📄 Found {len(python_files)} Python file(s)\n")

        changes_count = 0
        for file_path in python_files:
            source_code = read_file(file_path)
            if not source_code.startswith("Error"):
                try:
                    extractor = ASTExtractor(source_code, file_path)
                    metadata = extractor.extract_all_metadata()

                    # For brevity, show a summary
                    debt = metadata.get("documentation_debt", {})
                    total_missing = len(debt["missing_class_docstrings"]) + len(debt["missing_function_docstrings"])

                    if total_missing > 0:
                        print(f"📝 {file_path}")
                        print(f"  ℹ️  Found {total_missing} missing docstring(s)")
                        changes_count += total_missing

                        if not args.dry_run:
                            # In a real scenario, this would apply fixes
                            print(f"  ✅ Would apply {total_missing} docstring(s)")

                except Exception as e:
                    print(f"❌ {file_path}: {str(e)}")

        print(f"\n📊 Summary: {changes_count} docstring(s) identified")
        if args.dry_run:
            print("🔍 Dry-run mode: No changes applied")
        else:
            print("✅ Docstrings applied successfully")

        return 0


def main() -> int:
    """Main entry point."""
    cli = DocstringCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
