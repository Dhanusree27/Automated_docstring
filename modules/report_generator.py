"""
Report Generator Module.

Generates comprehensive docstring coverage reports in multiple formats.
"""
import json
from typing import Dict, List, Any
from datetime import datetime


class ReportGenerator:
    """Generate reports on docstring coverage and quality."""

    def __init__(self):
        """Initialize the report generator."""
        self.reports = []

    def generate_project_report(
        self,
        project_name: str,
        files_metadata: List[Dict[str, Any]],
        coverage_reports: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive project report.

        Args:
            project_name: Name of the project.
            files_metadata: List of metadata from all analyzed files.
            coverage_reports: List of coverage reports from all files.

        Returns:
            Comprehensive project report dictionary.
        """
        total_coverage = self._calculate_total_coverage(coverage_reports)
        compliance_status = self._get_compliance_status(total_coverage)

        report = {
            "project_name": project_name,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_files": len(files_metadata),
                "overall_coverage": total_coverage,
                "compliance_status": compliance_status,
                "total_classes": sum(c["classes"]["total"] for c in coverage_reports),
                "total_functions": sum(f["functions"]["total"] for f in coverage_reports),
                "documented_classes": sum(c["classes"]["documented"] for c in coverage_reports),
                "documented_functions": sum(f["functions"]["documented"] for f in coverage_reports)
            },
            "file_reports": coverage_reports,
            "statistics": self._generate_statistics(coverage_reports),
            "recommendations": self._generate_recommendations(total_coverage)
        }

        self.reports.append(report)
        return report

    def generate_json_report(self, report: Dict[str, Any]) -> str:
        """
        Convert report to JSON format.

        Args:
            report: The report dictionary.

        Returns:
            JSON string representation of the report.
        """
        return json.dumps(report, indent=2, default=str)

    def generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """
        Generate a markdown report.

        Args:
            report: The report dictionary.

        Returns:
            Markdown formatted report.
        """
        md = []
        md.append(f"# Docstring Coverage Report - {report['project_name']}")
        md.append(f"\n**Generated:** {report['generated_at']}\n")

        # Summary Section
        summary = report["summary"]
        md.append("## Summary")
        md.append(f"- **Overall Coverage:** {summary['overall_coverage']:.2f}%")
        md.append(f"- **Compliance Status:** {summary['compliance_status']}")
        md.append(f"- **Total Files:** {summary['total_files']}")
        md.append(f"- **Total Classes:** {summary['total_classes']} (Documented: {summary['documented_classes']})")
        md.append(f"- **Total Functions:** {summary['total_functions']} (Documented: {summary['documented_functions']})\n")

        # File Details
        md.append("## File Details")
        md.append("| File | Coverage | Classes | Functions | Status |")
        md.append("|------|----------|---------|-----------|--------|")

        for file_report in report["file_reports"]:
            coverage = file_report["overall_coverage"]
            status = self._get_coverage_emoji(coverage)
            md.append(
                f"| {file_report['file_path']} | {coverage:.1f}% | "
                f"{file_report['classes']['total']} | "
                f"{file_report['functions']['total']} | {status} |"
            )

        md.append("")

        # Statistics
        stats = report["statistics"]
        md.append("## Statistics")
        md.append(f"- **Average File Coverage:** {stats['average_coverage']:.2f}%")
        md.append(f"- **Highest Coverage:** {stats['highest_coverage']:.2f}%")
        md.append(f"- **Lowest Coverage:** {stats['lowest_coverage']:.2f}%")
        md.append(f"- **Compliant Files:** {stats['compliant_files']}")
        md.append(f"- **Warning Files:** {stats['warning_files']}")
        md.append(f"- **Critical Files:** {stats['critical_files']}\n")

        # Recommendations
        md.append("## Recommendations")
        for rec in report["recommendations"]:
            md.append(f"- {rec}")

        return "\n".join(md)

    def generate_html_report(self, report: Dict[str, Any]) -> str:
        """
        Generate an HTML report.

        Args:
            report: The report dictionary.

        Returns:
            HTML representation of the report.
        """
        summary = report["summary"]
        stats = report["statistics"]

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docstring Coverage Report - {report['project_name']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }}
        h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .timestamp {{ opacity: 0.9; font-size: 0.9em; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .card h3 {{ color: #667eea; margin-bottom: 10px; font-size: 1.2em; }}
        .card-value {{ font-size: 2em; font-weight: bold; color: #333; }}
        .progress-bar {{ width: 100%; height: 8px; background: #e0e0e0; border-radius: 4px; overflow: hidden; margin-top: 10px; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #667eea; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #e0e0e0; }}
        tr:hover {{ background: #f9f9f9; }}
        .status-excellent {{ color: #28a745; }}
        .status-good {{ color: #17a2b8; }}
        .status-fair {{ color: #ffc107; }}
        .status-poor {{ color: #dc3545; }}
        footer {{ margin-top: 40px; padding: 20px; text-align: center; color: #666; border-top: 1px solid #e0e0e0; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Docstring Coverage Report</h1>
            <p>{report['project_name']}</p>
            <p class="timestamp">Generated: {report['generated_at']}</p>
        </header>

        <div class="summary">
            <div class="card">
                <h3>Overall Coverage</h3>
                <div class="card-value">{summary['overall_coverage']:.1f}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(summary['overall_coverage'], 100)}%"></div>
                </div>
            </div>
            <div class="card">
                <h3>Source Files</h3>
                <div class="card-value">{summary['total_files']}</div>
            </div>
            <div class="card">
                <h3>Classes</h3>
                <div class="card-value">{summary['total_classes']}</div>
                <p>Documented: {summary['documented_classes']}</p>
            </div>
            <div class="card">
                <h3>Functions</h3>
                <div class="card-value">{summary['total_functions']}</div>
                <p>Documented: {summary['documented_functions']}</p>
            </div>
        </div>

        <h2>File Details</h2>
        <table>
            <thead>
                <tr>
                    <th>File</th>
                    <th>Coverage</th>
                    <th>Classes</th>
                    <th>Functions</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
"""

        for file_report in report["file_reports"]:
            coverage = file_report["overall_coverage"]
            status_class = self._get_status_class(coverage)
            html += f"""                <tr>
                    <td>{file_report['file_path']}</td>
                    <td><strong>{coverage:.1f}%</strong></td>
                    <td>{file_report['classes']['total']}</td>
                    <td>{file_report['functions']['total']}</td>
                    <td class="{status_class}">{file_report['coverage_level']}</td>
                </tr>
"""

        html += f"""            </tbody>
        </table>

        <h2 style="margin-top: 30px;">Statistics</h2>
        <div class="summary" style="margin-top: 20px;">
            <div class="card">
                <h3>Average Coverage</h3>
                <div class="card-value">{stats['average_coverage']:.1f}%</div>
            </div>
            <div class="card">
                <h3>Highest Coverage</h3>
                <div class="card-value">{stats['highest_coverage']:.1f}%</div>
            </div>
            <div class="card">
                <h3>Lowest Coverage</h3>
                <div class="card-value">{stats['lowest_coverage']:.1f}%</div>
            </div>
            <div class="card">
                <h3>Compliant Files</h3>
                <div class="card-value">{stats['compliant_files']}</div>
            </div>
        </div>

        <footer>
            <p>Generated by Automated Python Docstring Generator</p>
        </footer>
    </div>
</body>
</html>"""

        return html

    def _calculate_total_coverage(self, coverage_reports: List[Dict[str, Any]]) -> float:
        """Calculate total project coverage."""
        if not coverage_reports:
            return 0.0

        total_documented = sum(
            c["classes"]["documented"] + c["functions"]["documented"]
            for c in coverage_reports
        )
        total_items = sum(
            c["classes"]["total"] + c["functions"]["total"]
            for c in coverage_reports
        )

        return (total_documented / total_items * 100) if total_items > 0 else 0.0

    def _get_compliance_status(self, coverage: float) -> str:
        """Get compliance status based on coverage percentage."""
        if coverage >= 95:
            return "✅ Excellent"
        elif coverage >= 80:
            return "✓ Good"
        elif coverage >= 60:
            return "⚠ Fair"
        else:
            return "❌ Poor"

    def _generate_statistics(self, coverage_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate statistics from coverage reports."""
        if not coverage_reports:
            return {
                "average_coverage": 0.0,
                "highest_coverage": 0.0,
                "lowest_coverage": 0.0,
                "compliant_files": 0,
                "warning_files": 0,
                "critical_files": 0
            }

        coverages = [c["overall_coverage"] for c in coverage_reports]

        compliant = sum(1 for c in coverages if c >= 95)
        warning = sum(1 for c in coverages if 60 <= c < 95)
        critical = sum(1 for c in coverages if c < 60)

        return {
            "average_coverage": sum(coverages) / len(coverages),
            "highest_coverage": max(coverages),
            "lowest_coverage": min(coverages),
            "compliant_files": compliant,
            "warning_files": warning,
            "critical_files": critical
        }

    def _generate_recommendations(self, coverage: float) -> List[str]:
        """Generate recommendations based on coverage."""
        recommendations = []

        if coverage >= 95:
            recommendations.append("✅ Excellent coverage! Continue maintaining these standards.")
        elif coverage >= 80:
            recommendations.append("📈 Good coverage. Focus on documenting the remaining items.")
            recommendations.append("🎯 Target: Increase coverage to 95% for excellence.")
        elif coverage >= 60:
            recommendations.append("⚠️ Fair coverage. Significant documentation effort needed.")
            recommendations.append("📋 Priority: Document all public APIs and classes.")
        else:
            recommendations.append("🚨 Critical coverage issue. Comprehensive documentation required.")
            recommendations.append("💡 Start with: Document all public classes and functions.")

        recommendations.append("💡 Use the CLI tool to automatically generate docstrings.")

        return recommendations

    def _get_coverage_emoji(self, coverage: float) -> str:
        """Get emoji for coverage level."""
        if coverage >= 95:
            return "✅"
        elif coverage >= 80:
            return "✓"
        elif coverage >= 60:
            return "⚠"
        else:
            return "❌"

    def _get_status_class(self, coverage: float) -> str:
        """Get CSS class for coverage status."""
        if coverage >= 95:
            return "status-excellent"
        elif coverage >= 80:
            return "status-good"
        elif coverage >= 60:
            return "status-fair"
        else:
            return "status-poor"
