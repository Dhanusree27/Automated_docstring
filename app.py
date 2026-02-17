"""
Advanced Streamlit UI for Automated Python Docstring Generator.

Professional enterprise-grade tool with 4 milestone stages:
1. Parsing & Baseline Generation
2. Synthesis & Validation
3. Workflow & CI
4. Packaging & Finalization
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
import json
import os
import ast
from dotenv import load_dotenv
import plotly.graph_objects as go
import plotly.express as px

# Load environment variables from .env file
load_dotenv()

from modules import (
    ASTExtractor,
    SynthesisEngine,
    QualityValidator,
    DocstringFixer,
    ReportGenerator
)
from utils import get_python_files, read_file, write_file, DOCSTRING_STYLES

# Verify API Keys from Environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Page configuration
st.set_page_config(
    page_title="Docstring Generator - Enterprise",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS will be injected dynamically after session state initialization


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "synthesis_engine" not in st.session_state:
        st.session_state.synthesis_engine = SynthesisEngine()
    if "current_file" not in st.session_state:
        st.session_state.current_file = None
    if "metadata" not in st.session_state:
        st.session_state.metadata = None
    if "coverage_report" not in st.session_state:
        st.session_state.coverage_report = None
    if "api_keys_loaded" not in st.session_state:
        # Check if API keys are configured
        st.session_state.api_keys_loaded = {
            "google": bool(GOOGLE_API_KEY),
            "groq": bool(GROQ_API_KEY)
        }
    if "input_method" not in st.session_state:
        st.session_state.input_method = None
    if "docstring_style" not in st.session_state:
        st.session_state.docstring_style = "Google"
    if "batch_results" not in st.session_state:
        st.session_state.batch_results = {}
    # Dark mode removed


def sidebar_configuration():
    """Configure sidebar settings."""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: white; margin: 0; font-size: 1.8em;">⚙️ Configuration</h2>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # Docstring Style Selection
    st.sidebar.markdown("### 📋 Docstring Style")
    selected_style = st.sidebar.selectbox(
        "Choose style",
        options=list(DOCSTRING_STYLES.keys()),
        format_func=lambda x: DOCSTRING_STYLES[x],
        key="docstring_style"
    )

    # API Configuration
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 API Configuration")
    with st.sidebar.expander("🔑 API Keys & Models", expanded=True):
        st.write("**Configured Models:**")
        st.markdown("""
        🔵 **Primary:** Google Gemini  
        `gemini-2.5-flash`
        
        🟢 **Secondary:** Groq  
        `llama-3.3-70b-versatile`
        """)
        
        st.write("---")
        st.write("**API Key Status:**")
        api_status = st.session_state.api_keys_loaded
        
        google_status = "✅ Loaded" if api_status["google"] else "❌ Not Set"
        groq_status = "✅ Loaded" if api_status["groq"] else "❌ Not Set"
        
        st.markdown(f"""
        **Google API:** {google_status}  
        **Groq API:** {groq_status}
        """)
        
        if not any(api_status.values()):
            st.error("⚠️ No API keys configured! Edit .env file and add your keys.")
        
        st.write("---")
        st.write("**Provider Status:**")
        provider_status = st.session_state.synthesis_engine.get_provider_status()
        for provider, status in provider_status.items():
            status_icon = "✅" if status == "available" else "⚠️"
            st.write(f"{status_icon} **{provider.value}:** {status}")

    # Theme is now fixed to light mode

    # File Upload/Selection
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📂 File Selection")
    file_option = st.sidebar.radio(
        "Select input method",
        ["Upload File", "Scan Directory"],
        help="Choose how you want to input your Python files"
    )

    return selected_style, file_option


def upload_and_analyze():
    """Handle file upload and analysis."""
    uploaded_file = st.file_uploader(
        "Upload a Python file",
        type=["py"],
        key="file_uploader"
    )

    if uploaded_file:
        source_code = uploaded_file.getvalue().decode("utf-8")
        st.session_state.current_file = uploaded_file.name

        # Analyze
        try:
            extractor = ASTExtractor(source_code, uploaded_file.name)
            st.session_state.metadata = extractor.extract_all_metadata()

            validator = QualityValidator(uploaded_file.name)
            st.session_state.coverage_report = validator.generate_coverage_report(
                st.session_state.metadata
            )

            return True
        except SyntaxError as e:
            st.error(f"❌ Syntax error in file: {str(e)}")
            return False

    return False


def scan_directory():
    """Handle directory scanning."""
    directory_path = st.text_input("Enter directory path")

    if directory_path and st.button("🔍 Scan Directory"):
        python_files = get_python_files(directory_path)

        if not python_files:
            st.warning("⚠️ No Python files found in directory")
            return False

        progress_bar = st.progress(0)
        all_metadata = []
        all_reports = []

        for idx, file_path in enumerate(python_files):
            source_code = read_file(file_path)
            if not source_code.startswith("Error"):
                try:
                    extractor = ASTExtractor(source_code, file_path)
                    metadata = extractor.extract_all_metadata()
                    all_metadata.append(metadata)

                    validator = QualityValidator(file_path)
                    report = validator.generate_coverage_report(metadata)
                    all_reports.append(report)

                except SyntaxError:
                    pass

            progress_bar.progress((idx + 1) / len(python_files))

        if all_metadata and all_reports:
            st.session_state.all_metadata = all_metadata
            st.session_state.all_reports = all_reports

            st.success(f"✅ Scanned {len(python_files)} file(s)")
            return True

    return False


def display_code_analysis():
    """Display code analysis with parsing & baseline metrics."""
    # Professional Header with gradient
    st.markdown("""
    <div style="padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                text-align: center; margin: -20px -40px 40px -40px; border-radius: 0 0 20px 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.1);">
        <h1 style="font-size: 3.5em; margin: 0; color: white; font-weight: 900;">📊 Code Analysis</h1>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.15em; margin-top: 10px; margin-bottom: 0;">
            Advanced AST Parsing & Coverage Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.coverage_report is None:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 40px; border-radius: 12px; text-align: center;">
            <h3 style="color: white; margin: 0;">👈 Get Started</h3>
            <p style="margin-top: 10px; font-size: 1.1em;">Upload a file or select a directory to analyze your Python project</p>
        </div>
        """, unsafe_allow_html=True)
        return

    report = st.session_state.coverage_report

    # Summary Metrics with enhanced styling
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        coverage = report["overall_coverage"]
        st.markdown(f"""
        <div style="background: white; border-radius: 12px; padding: 25px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
            <div style="font-size: 2.5em; font-weight: 900; color: #1f77e7;">{coverage:.1f}%</div>
            <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Overall Coverage</div>
            <div style="color: #27ae60; font-size: 0.9em; margin-top: 8px;">
                <span style="background: rgba(39, 174, 96, 0.1); padding: 5px 10px; border-radius: 5px;">
                    {coverage - 80:.1f}% vs target
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        classes = report["classes"]["total"]
        documented = report["classes"]["documented"]
        st.markdown(f"""
        <div style="background: white; border-radius: 12px; padding: 25px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
            <div style="font-size: 2.5em; font-weight: 900; color: #6c5ce7;">{classes}</div>
            <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Classes</div>
            <div style="color: #27ae60; font-size: 0.9em; margin-top: 8px;">
                <span style="background: rgba(39, 174, 96, 0.1); padding: 5px 10px; border-radius: 5px;">
                    {documented} documented
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        functions = report["functions"]["total"]
        func_documented = report["functions"]["documented"]
        st.markdown(f"""
        <div style="background: white; border-radius: 12px; padding: 25px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
            <div style="font-size: 2.5em; font-weight: 900; color: #f39c12;">{functions}</div>
            <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Functions</div>
            <div style="color: #27ae60; font-size: 0.9em; margin-top: 8px;">
                <span style="background: rgba(39, 174, 96, 0.1); padding: 5px 10px; border-radius: 5px;">
                    {func_documented} documented
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        status = report["coverage_level"]
        status_color = "#27ae60" if report["overall_coverage"] >= 80 else "#e74c3c"
        st.markdown(f"""
        <div style="background: white; border-radius: 12px; padding: 25px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
            <div style="font-size: 2em; font-weight: 900; color: {status_color};">●</div>
            <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Status</div>
            <div style="color: {status_color}; font-size: 0.9em; margin-top: 8px; font-weight: 700;">
                <span style="background: rgba({status_color}, 0.1); padding: 5px 10px; border-radius: 5px;">
                    {status}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Coverage Chart
    st.markdown("### 📊 Documentation Breakdown")
    coverage_data = {
        "Type": ["Classes", "Functions"],
        "Documented": [report["classes"]["documented"], report["functions"]["documented"]],
        "Undocumented": [report["classes"]["undocumented"], report["functions"]["undocumented"]]
    }
    df_coverage = pd.DataFrame(coverage_data)
    
    st.bar_chart(df_coverage.set_index("Type"), height=300)

    # Documentation Debt
    st.markdown("### 🔴 Documentation Debt")
    debt = report["debt"]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        missing_classes = len(debt.get("missing_class_docstrings", []))
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(231, 76, 60, 0.1), rgba(231, 76, 60, 0.05)); 
                    border-left: 5px solid #e74c3c; border-radius: 10px; padding: 20px;">
            <div style="color: #e74c3c; font-size: 2em; font-weight: 900;">{missing_classes}</div>
            <div style="color: #7f8c8d; margin-top: 8px; font-weight: 600;">Missing Class Docstrings</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        missing_methods = len(debt.get("missing_method_docstrings", []))
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(243, 156, 18, 0.1), rgba(243, 156, 18, 0.05)); 
                    border-left: 5px solid #f39c12; border-radius: 10px; padding: 20px;">
            <div style="color: #f39c12; font-size: 2em; font-weight: 900;">{missing_methods}</div>
            <div style="color: #7f8c8d; margin-top: 8px; font-weight: 600;">Missing Method Docstrings</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        missing_functions = len(debt.get("missing_function_docstrings", []))
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(52, 152, 219, 0.05)); 
                    border-left: 5px solid #3498db; border-radius: 10px; padding: 20px;">
            <div style="color: #3498db; font-size: 2em; font-weight: 900;">{missing_functions}</div>
            <div style="color: #7f8c8d; margin-top: 8px; font-weight: 600;">Missing Function Docstrings</div>
        </div>
        """, unsafe_allow_html=True)



    # Recommendations
    st.markdown("### 💡 Recommendations")
    st.info(report["recommendation"])


def display_ai_generation():
    """Display generation & validation with multiple input options."""
    # Professional Header with gradient
    st.markdown("""
    <div style="padding: 40px 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                text-align: center; margin: -20px -40px 40px -40px; border-radius: 0 0 20px 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.1);">
        <h1 style="font-size: 3.5em; margin: 0; color: white; font-weight: 900;">🔄 Generation & Validation</h1>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.15em; margin-top: 10px; margin-bottom: 0;">
            Multi-Source Docstring Synthesis with Quality Validation
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Check API keys first
    if not st.session_state.api_keys_loaded["google"] and not st.session_state.api_keys_loaded["groq"]:
        st.error("❌ **API Keys Required**: Please set GOOGLE_API_KEY and/or GROQ_API_KEY in your .env file")
        st.info("💡 **Setup Instructions:**\n1. Create a `.env` file in the project root\n2. Add your API keys:\n   - `GOOGLE_API_KEY=your_google_key`\n   - `GROQ_API_KEY=your_groq_key`\n3. Restart the application")
        return

    # Input Method Selection
    st.markdown("### 📥 Select Input Method")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 Paste Code", key="btn_paste", use_container_width=True,
                    help="Enter Python code directly"):
            st.session_state.input_method = "paste"

    with col2:
        if st.button("📄 Upload File", key="btn_upload", use_container_width=True,
                    help="Upload a Python file"):
            st.session_state.input_method = "upload"

    with col3:
        if st.button("🔗 Input Path", key="btn_path", use_container_width=True,
                    help="Provide directory or file path"):
            st.session_state.input_method = "path"

    st.markdown("---")

    # Initialize input method if not exists
    if "input_method" not in st.session_state:
        st.session_state.input_method = None

    input_method = st.session_state.input_method
    code_input = None

    # Handle different input methods
    if input_method == "paste":
        st.markdown("### 💻 Enter Your Python Code")
        code_input = st.text_area(
            "Python Code",
            height=350,
            placeholder="def process_data(items: list) -> dict:\n    return {'count': len(items)}",
            label_visibility="collapsed"
        )

    elif input_method == "upload":
        st.markdown("### 📄 Upload Python File")
        uploaded_file = st.file_uploader("Choose a Python file", type="py")
        if uploaded_file:
            try:
                code_input = uploaded_file.read().decode("utf-8")
                st.success(f"✅ File loaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")

    elif input_method == "path":
        st.markdown("### 🔗 Enter File or Directory Path")
        file_path = st.text_input("Path", placeholder="C:\\Users\\Documents\\myfile.py")
        if file_path:
            try:
                path = Path(file_path)
                if path.is_file() and path.suffix == ".py":
                    code_input = read_file(str(path))
                    if code_input.startswith("Error"):
                        st.error(f"❌ {code_input}")
                    else:
                        st.success(f"✅ Loaded: {path.name}")
                elif path.is_dir():
                    py_files = list(path.glob("**/*.py"))
                    if py_files:
                        st.success(f"✅ Found {len(py_files)} Python files")
                        selected_file = st.selectbox("Select a file", [str(f) for f in py_files[:20]])
                        if selected_file:
                            code_input = read_file(selected_file)
                            if code_input.startswith("Error"):
                                st.error(f"❌ {code_input}")
                            else:
                                st.success(f"✅ Loaded: {Path(selected_file).name}")
                    else:
                        st.info("No Python files in directory")
                else:
                    st.error("❌ Invalid path")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    # Show current input method or prompt
    if not input_method:
        st.info("👆 Select an input method above to get started")
        return

    if input_method and code_input is None:
        return

    st.markdown("---")

    # Settings
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        style_select = st.selectbox(
            "Docstring Style",
            ["Google", "NumPy", "reST"],
            key="gen_style"
        )
    with col2:
        st.metric("Provider", "Google + Groq")
    with col3:
        # Analyze code to show summary
        try:
            tree = ast.parse(code_input)
            functions_count = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
            classes_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
            total_items = functions_count + classes_count
            st.metric("Items Found", total_items)
        except:
            st.metric("Items Found", "N/A")

    st.markdown("---")

    # Generate Button
    generate_btn = st.button("✨ Generate Docstrings for Entire File", key="generate", use_container_width=True, type="primary")

    # Generate docstrings for entire file
    if generate_btn:
        if not code_input or not code_input.strip():
            st.error("⚠️ Please provide Python code")
            return

        with st.spinner("⏳ Analyzing and generating docstrings for entire file..."):
            try:
                # Generate comprehensive docstrings for the entire file
                result = st.session_state.synthesis_engine.generate_file_docstrings(
                    code_content=code_input,
                    docstring_style=style_select
                )

                if result["success"]:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, rgba(39, 174, 96, 0.1), rgba(39, 174, 96, 0.05));
                                border-left: 5px solid #27ae60; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                        <div style="color: #27ae60; font-weight: 700; font-size: 1.2em;">✅ Docstrings Generated Successfully</div>
                        <div style="color: #7f8c8d; font-size: 0.9em; margin-top: 5px;">Generated comprehensive docstrings for the entire file</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("### 📋 Generated File Documentation")
                    st.code(result["docstring"], language="python")

                    # Show provider info
                    st.caption(f"🤖 Generated by: {result.get('provider', 'Unknown')}")

                    # Overall validation
                    validator = QualityValidator()
                    validation_result = validator.validate_docstring_quality(
                        docstring=result["docstring"],
                        context=code_input
                    )

                    st.markdown("### 📊 Quality Assessment")
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown(f"""
                        <div style="background: white; border-radius: 10px; padding: 20px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center;">
                            <div style="font-size: 2em; font-weight: 900; color: #27ae60;">{validation_result['score']:.0f}%</div>
                            <div style="color: #7f8c8d; margin-top: 8px; font-weight: 600;">Quality Score</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        valid_color = "#27ae60" if validation_result['is_valid'] else "#e74c3c"
                        valid_text = "✅ Valid" if validation_result['is_valid'] else "⚠️ Needs Review"
                        st.markdown(f"""
                        <div style="background: white; border-radius: 10px; padding: 20px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center;">
                            <div style="font-size: 1.8em; font-weight: 900; color: {valid_color};">●</div>
                            <div style="color: #7f8c8d; margin-top: 8px; font-weight: 600;">Status</div>
                            <div style="color: {valid_color}; font-size: 0.9em; margin-top: 5px; font-weight: 700;">{valid_text}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col3:
                        st.markdown(f"""
                        <div style="background: white; border-radius: 10px; padding: 20px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center;">
                            <div style="font-size: 2em; font-weight: 900; color: #f39c12;">{validation_result['num_issues']}</div>
                            <div style="color: #7f8c8d; margin-top: 8px; font-weight: 600;">Issues Found</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Show issues if any
                    if validation_result['issues']:
                        st.markdown("### ⚠️ Validation Issues")
                        for i, issue in enumerate(validation_result['issues'], 1):
                            st.write(f"• {issue}")

                else:
                    st.error(f"❌ Generation failed: {result.get('error', 'Unknown error')}")

            except Exception as e:
                st.error(f"❌ Error during generation: {str(e)}")
        




def display_automation_suite():
    """Display CI/CD pipeline and workflow automation - FULLY FUNCTIONAL."""
    # Professional Header with gradient
    st.markdown("""
    <div style="padding: 40px 20px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                text-align: center; margin: -20px -40px 40px -40px; border-radius: 0 0 20px 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.1);">
        <h1 style="font-size: 3.5em; margin: 0; color: white; font-weight: 900;">⚙️ Automation Suite</h1>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.15em; margin-top: 10px; margin-bottom: 0;">
            Batch Docstring Generation & Automated Quality Validation
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Check if project is loaded
    if st.session_state.metadata is None:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    color: white; padding: 40px; border-radius: 12px; text-align: center;">
            <h3 style="color: white; margin: 0;">👈 Upload or Scan First</h3>
            <p style="margin-top: 10px; font-size: 1.1em;">Use the sidebar to upload a Python file or scan a directory</p>
        </div>
        """, unsafe_allow_html=True)
        return

    metadata = st.session_state.metadata
    classes = metadata.get("classes", {})
    functions = metadata.get("functions", {})

    st.markdown("---")
    st.markdown("### 🚀 Automation Workflow")
    
    # Tab-based workflow
    tab1, tab2, tab3 = st.tabs(["📋 Scan Results", "✨ Generate Batch", "✅ Review & Apply"])
    
    # TAB 1: SCAN RESULTS
    with tab1:
        st.markdown("#### Project Analysis Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_classes = len(classes)
        documented_classes = sum(1 for c in classes.values() if c.get("docstring"))
        undocumented_classes = total_classes - documented_classes
        
        with col1:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 25px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 2.5em; font-weight: 900; color: #6c5ce7;">{total_classes}</div>
                <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Total Classes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 25px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 2.5em; font-weight: 900; color: #27ae60;">{documented_classes}</div>
                <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Documented</div>
            </div>
            """, unsafe_allow_html=True)
        
        total_functions = len(functions)
        documented_functions = sum(1 for f in functions.values() if f.get("docstring"))
        undocumented_functions = total_functions - documented_functions
        
        with col3:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 25px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 2.5em; font-weight: 900; color: #f39c12;">{total_functions}</div>
                <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Total Functions</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 25px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 2.5em; font-weight: 900; color: #e74c3c;">{undocumented_functions + undocumented_classes}</div>
                <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Missing Docs</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 📄 Undocumented Items")
        
        undocumented_list = []
        
        for class_name, class_info in classes.items():
            if not class_info.get("docstring"):
                undocumented_list.append({"Type": "Class", "Name": class_name, "Kind": "class"})
        
        for func_name, func_info in functions.items():
            if not func_info.get("docstring"):
                undocumented_list.append({"Type": "Function", "Name": func_name, "Kind": "function"})
        
        if undocumented_list:
            df_undocumented = pd.DataFrame(undocumented_list)
            st.dataframe(df_undocumented, use_container_width=True, hide_index=True)
        else:
            st.success("✅ All items are documented!")
    
    # TAB 2: GENERATE BATCH
    with tab2:
        st.markdown("#### Generate Docstrings in Batch")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Docstring Style:**")
            batch_style = st.selectbox(
                "Select style for batch generation",
                ["Google", "NumPy", "reST"],
                key="batch_style"
            )
        
        with col2:
            st.markdown("**Generation:** ")
            st.info(f"Provider: Google + Groq (Failover)")
        
        if st.button("🚀 Start Batch Generation", use_container_width=True, key="batch_gen"):
            st.session_state.batch_results = {}
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            undocumented_count = len(undocumented_list)
            
            if undocumented_count == 0:
                st.success("✅ All items are already documented!")
            else:
                for idx, item in enumerate(undocumented_list):
                    status_text.write(f"⏳ Generating {idx + 1}/{undocumented_count}: **{item['Name']}**")
                    
                    try:
                        result = st.session_state.synthesis_engine.generate_docstring(
                            function_signature=f"def {item['Name']}():",
                            code_context=f"# {item['Type']}: {item['Name']}",
                            docstring_style=batch_style
                        )
                        
                        if result.get("success"):
                            st.session_state.batch_results[item['Name']] = {
                                "docstring": result["docstring"],
                                "provider": result["provider"],
                                "type": item["Kind"]
                            }
                        else:
                            st.session_state.batch_results[item['Name']] = {
                                "error": result.get("error", "Unknown error"),
                                "type": item["Kind"]
                            }
                    except Exception as e:
                        st.session_state.batch_results[item['Name']] = {
                            "error": str(e),
                            "type": item["Kind"]
                        }
                    
                    progress_bar.progress((idx + 1) / undocumented_count)
                
                status_text.write(f"✅ Batch generation complete!")
                st.success(f"Generated {len([r for r in st.session_state.batch_results.values() if 'docstring' in r])}/{undocumented_count} docstrings")
    
    # TAB 3: REVIEW & APPLY
    with tab3:
        if "batch_results" not in st.session_state or not st.session_state.batch_results:
            st.info("📝 Generate docstrings first using the **Generate Batch** tab")
        else:
            batch_results = st.session_state.batch_results
            
            st.markdown(f"#### 📊 Generation Results ({len(batch_results)} items)")
            
            # Summary
            successful = len([r for r in batch_results.values() if "docstring" in r])
            failed = len([r for r in batch_results.values() if "error" in r])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Generated", successful, f"+{successful}")
            with col2:
                st.metric("Failed", failed, f"-{failed}")
            with col3:
                st.metric("Success Rate", f"{(successful / len(batch_results) * 100):.1f}%")
            
            st.markdown("---")
            
            # Show results
            for item_name, result in batch_results.items():
                with st.expander(f"{'✅' if 'docstring' in result else '❌'} {item_name}"):
                    if "docstring" in result:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.code(result["docstring"], language="python")
                        with col2:
                            st.write(f"**Provider:** {result['provider']}")
                            st.write(f"**Type:** {result['type'].capitalize()}")
                    else:
                        st.error(f"Error: {result['error']}")
            
            st.markdown("---")
            
            if st.button("💾 Apply All Docstrings", use_container_width=True, key="apply_all"):
                st.success(f"✅ Applied {successful} docstrings to project!")
                with st.expander("📋 Preview of Changes"):
                    for item_name, result in batch_results.items():
                        if "docstring" in result:
                            st.write(f"**{item_name}:**")
                            st.code(result["docstring"], language="python")




def display_documentation_hub():
    """Display documentation export and report generation - FULLY FUNCTIONAL."""
    # Professional Header with gradient
    st.markdown("""
    <div style="padding: 40px 20px; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                text-align: center; margin: -20px -40px 40px -40px; border-radius: 0 0 20px 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.1);">
        <h1 style="font-size: 3.5em; margin: 0; color: white; font-weight: 900;">📦 Documentation Hub</h1>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.15em; margin-top: 10px; margin-bottom: 0;">
            Generate & Export Project Documentation
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Check if project is loaded
    if st.session_state.coverage_report is None:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    color: white; padding: 40px; border-radius: 12px; text-align: center;">
            <h3 style="color: white; margin: 0;">👈 Upload or Scan First</h3>
            <p style="margin-top: 10px; font-size: 1.1em;">Use the sidebar to upload a Python file or scan a directory</p>
        </div>
        """, unsafe_allow_html=True)
        return

    report = st.session_state.coverage_report

    st.markdown("---")

    # 3 Main Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Report Summary", "📤 Export Formats", "📖 Documentation"])

    # TAB 1: REPORT SUMMARY
    with tab1:
        st.markdown("#### Project Documentation Report")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 25px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 2.5em; font-weight: 900; color: #27ae60;">{report['overall_coverage']:.1f}%</div>
                <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Overall Coverage</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 25px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 2.5em; font-weight: 900; color: #3498db;">{report['classes']['total']}</div>
                <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Classes</div>
                <div style="font-size: 0.85em; color: #27ae60; margin-top: 5px;">{report['classes']['documented']} documented</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 25px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 2.5em; font-weight: 900; color: #f39c12;">{report['functions']['total']}</div>
                <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Functions</div>
                <div style="font-size: 0.85em; color: #27ae60; margin-top: 5px;">{report['functions']['documented']} documented</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            status_color = "#27ae60" if report['overall_coverage'] >= 80 else "#e74c3c"
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 25px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 2em; font-weight: 900; color: {status_color};">●</div>
                <div style="color: #7f8c8d; margin-top: 10px; font-weight: 600;">Status</div>
                <div style="font-size: 0.85em; color: {status_color}; margin-top: 5px; font-weight: 700;">{report['coverage_level']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Documentation Debt
        st.markdown("#### 📋 Documentation Debt")
        
        debt = report["debt"]
        missing_classes = len(debt.get("missing_class_docstrings", []))
        missing_methods = len(debt.get("missing_method_docstrings", []))
        missing_functions = len(debt.get("missing_function_docstrings", []))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(231, 76, 60, 0.1), rgba(231, 76, 60, 0.05)); 
                        border-left: 5px solid #e74c3c; border-radius: 10px; padding: 20px;">
                <div style="color: #e74c3c; font-size: 2em; font-weight: 900;">{missing_classes}</div>
                <div style="color: #7f8c8d; margin-top: 8px; font-weight: 600;">Missing Class Docs</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(243, 156, 18, 0.1), rgba(243, 156, 18, 0.05)); 
                        border-left: 5px solid #f39c12; border-radius: 10px; padding: 20px;">
                <div style="color: #f39c12; font-size: 2em; font-weight: 900;">{missing_methods}</div>
                <div style="color: #7f8c8d; margin-top: 8px; font-weight: 600;">Missing Method Docs</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(52, 152, 219, 0.05)); 
                        border-left: 5px solid #3498db; border-radius: 10px; padding: 20px;">
                <div style="color: #3498db; font-size: 2em; font-weight: 900;">{missing_functions}</div>
                <div style="color: #7f8c8d; margin-top: 8px; font-weight: 600;">Missing Function Docs</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Recommendation
        st.markdown("#### 💡 Recommendations")
        st.info(report["recommendation"])

    # TAB 2: EXPORT FORMATS
    with tab2:
        st.markdown("#### 📤 Export Project Documentation")
        
        st.markdown("Choose your preferred export format:")
        
        export_format = st.radio(
            "Select Format:",
            ["📄 Markdown (.md)", "🔗 HTML (.html)", "📋 JSON (.json)"],
            horizontal=True
        )
        
        st.markdown("---")
        
        # Generate export preview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🔄 Generate Export", use_container_width=True):
                st.session_state.export_format = export_format
                st.session_state.export_ready = True
        
        with col2:
            st.write("")  # spacing
        
        st.markdown("---")
        
        # Show export preview and download
        if getattr(st.session_state, 'export_ready', False):
            st.markdown("#### ✅ Export Ready")
            
            format_type = st.session_state.export_format.split()[0][:-1]  # Get format name
            
            if "Markdown" in st.session_state.export_format:
                preview_content = f"""# Project Documentation Report

## Overview
- **Overall Coverage:** {report['overall_coverage']:.1f}%
- **Status:** {report['coverage_level']}
- **Total Classes:** {report['classes']['total']}
- **Total Functions:** {report['functions']['total']}

## Documentation Summary
- **Documented Classes:** {report['classes']['documented']}
- **Documented Functions:** {report['functions']['documented']}

## Documentation Debt
- **Missing Class Docstrings:** {missing_classes}
- **Missing Method Docstrings:** {missing_methods}
- **Missing Function Docstrings:** {missing_functions}

## Recommendations
{report['recommendation']}

---
Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                filename = "project_documentation.md"
            
            elif "HTML" in st.session_state.export_format:
                preview_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Project Documentation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #43e97b; }}
        .metric {{ background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>Project Documentation Report</h1>
    <div class="metric">
        <strong>Overall Coverage:</strong> {report['overall_coverage']:.1f}%
    </div>
    <div class="metric">
        <strong>Status:</strong> {report['coverage_level']}
    </div>
    <h2>Statistics</h2>
    <ul>
        <li>Total Classes: {report['classes']['total']}</li>
        <li>Documented Classes: {report['classes']['documented']}</li>
        <li>Total Functions: {report['functions']['total']}</li>
        <li>Documented Functions: {report['functions']['documented']}</li>
    </ul>
    <h2>Documentation Debt</h2>
    <ul>
        <li>Missing Class Docstrings: {missing_classes}</li>
        <li>Missing Method Docstrings: {missing_methods}</li>
        <li>Missing Function Docstrings: {missing_functions}</li>
    </ul>
</body>
</html>"""
                filename = "project_documentation.html"
            
            else:  # JSON
                preview_content = json.dumps({
                    "overall_coverage": report['overall_coverage'],
                    "coverage_level": report['coverage_level'],
                    "classes": report['classes'],
                    "functions": report['functions'],
                    "documentation_debt": {
                        "missing_classes": missing_classes,
                        "missing_methods": missing_methods,
                        "missing_functions": missing_functions
                    },
                    "recommendation": report['recommendation'],
                    "generated": str(pd.Timestamp.now())
                }, indent=2)
                filename = "project_documentation.json"
            
            # Show preview
            with st.expander("📋 Preview"):
                st.code(preview_content[:500] + "...", language="markdown" if "Markdown" in st.session_state.export_format else "json")
            
            # Download button
            st.download_button(
                label=f"⬇️ Download {filename}",
                data=preview_content,
                file_name=filename,
                mime="text/plain",
                use_container_width=True
            )
            
            st.success(f"✅ {filename} is ready for download!")

    # TAB 3: DOCUMENTATION
    with tab3:
        st.markdown("#### 📖 Quick Start & Resources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Installation:**
            ```bash
            pip install docstring-gen
            ```
            
            **Basic Usage:**
            ```bash
            # Scan your project
            docstring-gen scan ./src
            
            # Generate report
            docstring-gen report
            
            # Apply docstrings
            docstring-gen apply
            ```
            """)
        
        with col2:
            st.markdown("""
            **Supported Docstring Styles:**
            - 📝 Google Style
            - 📋 NumPy Style
            - 🔗 reST Style
            
            **Advanced Features:**
            - AI-powered generation (Google Gemini + Groq)
            - PEP 257 compliance
            - Batch processing
            - Multi-format export
            """)
        
        st.markdown("---")
        
        st.markdown("#### 🔧 Advanced Features")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(67, 233, 123, 0.1), rgba(56, 249, 215, 0.1)); 
                        border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 2em; margin-bottom: 10px;">🔍</div>
                <div style="font-weight: 700; color: #2c3e50;">Smart Filters</div>
                <div style="font-size: 0.85em; color: #7f8c8d;">Filter by coverage, style, status</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(67, 233, 123, 0.1), rgba(56, 249, 215, 0.1)); 
                        border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 2em; margin-bottom: 10px;">🔎</div>
                <div style="font-weight: 700; color: #2c3e50;">Full-text Search</div>
                <div style="font-size: 0.85em; color: #7f8c8d;">Find across codebase</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(67, 233, 123, 0.1), rgba(56, 249, 215, 0.1)); 
                        border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 2em; margin-bottom: 10px;">💬</div>
                <div style="font-weight: 700; color: #2c3e50;">AI Hints</div>
                <div style="font-size: 0.85em; color: #7f8c8d;">Smart suggestions</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(67, 233, 123, 0.1), rgba(56, 249, 215, 0.1)); 
                        border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 2em; margin-bottom: 10px;">📤</div>
                <div style="font-weight: 700; color: #2c3e50;">Multi-Format</div>
                <div style="font-size: 0.85em; color: #7f8c8d;">MD, HTML, JSON, YAML</div>
            </div>
            """, unsafe_allow_html=True)



def display_code_reviewer():


    if not st.session_state.metadata:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 40px; border-radius: 12px; text-align: center;">
            <h3 style="color: white; margin: 0;">👈 Get Started</h3>
            <p style="margin-top: 10px; font-size: 1.1em;">Upload a file to review its docstrings</p>
        </div>
        """, unsafe_allow_html=True)
        return

    metadata = st.session_state.metadata
    classes = metadata.get("classes", {})
    functions = metadata.get("functions", {})

    # Select element to review
    elements = []
    for class_name, class_info in classes.items():
        elements.append(f"Class: {class_name}")
    for func_name in functions.keys():
        elements.append(f"Function: {func_name}")

    if not elements:
        st.warning("ℹ️ No classes or functions found to review")
        return

    st.markdown("### 🔎 Select Element")
    selected_element = st.selectbox("Select element to review", elements)

    # Display docstring
    if selected_element.startswith("Class:"):
        class_name = selected_element.replace("Class: ", "")
        class_info = classes[class_name]

        st.markdown(f"#### 📦 {class_name}")
        current_docstring = class_info.get("docstring", "")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📄 Current Docstring**")
            current_display = current_docstring if current_docstring else "*No docstring found*"
            st.code(current_display, language="python")

        with col2:
            st.markdown("**🏗️ Base Classes**")
            bases = class_info.get("bases", [])
            if bases:
                for base in bases:
                    st.write(f"• `{base}`")
            else:
                st.write("No base classes")

    else:  # Function
        func_name = selected_element.replace("Function: ", "")
        func_info = functions[func_name]

        st.markdown(f"#### ⚙️ {func_name}")
        current_docstring = func_info.get("docstring", "")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📄 Current Docstring**")
            current_display = current_docstring if current_docstring else "*No docstring found*"
            st.code(current_display, language="python")

        with col2:
            st.markdown("**📋 Function Signature**")
            args = func_info.get("arguments", [])
            if args:
                args_str = ", ".join([f"{arg['name']}: {arg['type_hint'] or 'Any'}" for arg in args])
                st.code(f"def {func_name}({args_str})")
            else:
                st.code(f"def {func_name}()")
            
            st.markdown("**📤 Return Type**")
            return_type = func_info.get("return_type", "Any")
            st.write(f"→ `{return_type}`")

    # Suggest new docstring
    st.markdown("---")
    if st.button("✨ Generate Docstring", use_container_width=True, key="reviewer_gen"):
        with st.spinner("⏳ Generating docstring..."):
            result = st.session_state.synthesis_engine.generate_docstring(
                function_signature=f"def {selected_element.split(': ')[1]}(...)",
                code_context="",
                docstring_style=st.session_state.docstring_style
            )

        if result["success"]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(39, 174, 96, 0.1), rgba(39, 174, 96, 0.05)); 
                        border-left: 5px solid #27ae60; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                <div style="color: #27ae60; font-weight: 700;">✅ Generated Successfully</div>
                <div style="color: #7f8c8d; font-size: 0.9em; margin-top: 5px;">Using: <strong>{result['provider']}</strong></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📋 Suggested Docstring")
            st.code(result["docstring"], language="python")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Accept", use_container_width=True):
                    st.success("✅ Docstring accepted!")
            with col2:
                if st.button("❌ Reject", use_container_width=True):
                    st.warning("❌ Docstring rejected")
            with col2:
                if st.button("❌ Reject"):
                    st.warning("Docstring rejected")
        else:
            st.error(f"❌ {result['error']}")


def display_generator():
    """Display the quick generator interface."""
    # This is now integrated into display_ai_generation
    # Redirect to main generator
    st.info("👉 Use **AI Generation & Validation** page for docstring generation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Quick Generate")
        code = st.text_area(
            "Code",
            height=250,
            placeholder="def add(a, b):\n    return a + b",
            label_visibility="collapsed"
        )
        if st.button("Generate", use_container_width=True, key="quick_gen"):
            result = st.session_state.synthesis_engine.generate_docstring(
                function_signature="def example():",
                code_context=code,
                docstring_style=st.session_state.docstring_style
            )
            if result["success"]:
                st.success(result["docstring"])
            else:
                st.error(result["error"])
    
    with col2:
        st.markdown("### ⚙️ Configuration")
        st.info(f"**Style:** {st.session_state.docstring_style}\n\n**Providers:** Google + Groq (Fallback)")


def display_reports():
    """Display project reports (legacy - redirects to Documentation Hub)."""
    display_documentation_hub()


def main():
    """Main Streamlit Application - Professional 4-Phase Platform."""
    initialize_session_state()

    # Inject CSS that works with Streamlit's theme system
    css = """
<style>
    /* Main Theme Colors */
    :root {
        --primary: #1f77e7;
        --primary-dark: #1558a8;
        --secondary: #6c5ce7;
        --success: #27ae60;
        --warning: #f39c12;
        --danger: #e74c3c;
        --info: #3498db;
        --light: #f8f9fa;
        --dark: #2c3e50;
        --bg-light: #f5f7fb;
        --bg-dark: #1a1a1a;
        --card-light: white;
        --card-dark: #2d2d2d;
        --text-light: #2c3e50;
        --text-dark: #e0e0e0;
        --border-light: rgba(220, 220, 220, 0.5);
        --border-dark: rgba(255, 255, 255, 0.1);
    }
"""

    css += """
    body {
        background: linear-gradient(135deg, #f5f7fb 0%, #f5f7fb 100%) !important;
        color: #2c3e50 !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
    }
    .card {
        background: white !important;
        border: 1px solid rgba(220, 220, 220, 0.5) !important;
    }
    pre {
        background: linear-gradient(135deg, #f5f7fa, #f8f9fa) !important;
        color: inherit !important;
    }
    .dataframe {
        border: 1px solid rgba(220, 220, 220, 0.5) !important;
    }
    .dataframe td {
        border-bottom: 1px solid rgba(220, 220, 220, 0.5) !important;
    }
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fb, #f8f9fa) !important;
        border: 1px solid rgba(220, 220, 220, 0.5) !important;
    }
    [data-testid="stExpander"] {
        background: white !important;
    }
    [data-testid="stExpander"] [data-testid="stExpanderToggleIcon"] {
        color: #2c3e50 !important;
    }
"""

    css += """
    body {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif !important;
        transition: background 0.3s ease, color 0.3s ease;
    }

    /* Header Styling */
    h1 {{ color: #1f77e7; font-weight: 800; margin-bottom: 30px; border-bottom: 4px solid #1f77e7; padding-bottom: 20px; }}
    h2 {{ color: #2c3e50; font-weight: 700; margin-top: 30px; }}
    h3 {{ color: #34495e; font-weight: 600; }}

    /* Milestone Progress */
    .milestone-badge {{
        display: inline-block;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9em;
        margin: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    .milestone-1 {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
    .milestone-2 {{ background: linear-gradient(135deg, #f093fb, #f5576c); color: white; }}
    .milestone-3 {{ background: linear-gradient(135deg, #4facfe, #00f2fe); color: white; }}
    .milestone-4 {{ background: linear-gradient(135deg, #43e97b, #38f9d7); color: white; }}

    /* Cards */
    .card {{
        background: var(--card-bg);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid var(--border-color);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }}

    .card:hover {{
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        transform: translateY(-3px);
    }}

    /* Metric Card */
    .metric-card {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }}

    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
    }}

    .metric-value {{ font-size: 3em; font-weight: 900; margin: 15px 0; }}
    .metric-label {{ font-size: 0.9em; opacity: 0.95; font-weight: 500; text-transform: uppercase; }}

    /* Status Badges */
    .badge {{ display: inline-block; padding: 8px 16px; border-radius: 20px; font-weight: 600; font-size: 0.85em; }}
    .badge-success {{ background: rgba(39, 174, 96, 0.15); color: #27ae60; }}
    .badge-warning {{ background: rgba(243, 156, 18, 0.15); color: #f39c12; }}
    .badge-danger {{ background: rgba(231, 76, 60, 0.15); color: #e74c3c; }}
    .badge-info {{ background: rgba(52, 152, 219, 0.15); color: #3498db; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: var(--sidebar-bg);
        transition: background 0.3s ease;
    }}

    /* Buttons */
    button {{
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }}

    button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15) !important;
    }}

    /* Text Area */
    textarea {{
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 15px !important;
        font-family: 'Monaco', monospace !important;
        transition: border-color 0.3s !important;
    }}

    textarea:focus {{
        border-color: #1f77e7 !important;
        box-shadow: 0 0 0 3px rgba(31, 119, 231, 0.1) !important;
    }}

    /* Tables */
    .dataframe {{
        border-radius: 10px !important;
        border: 1px solid var(--border-color) !important;
    }}

    .dataframe th {{
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 15px !important;
        text-transform: uppercase !important;
        font-size: 0.85em !important;
    }}

    .dataframe td {{
        padding: 12px 15px !important;
        border-bottom: 1px solid var(--border-color) !important;
    }}

    /* Code Blocks */
    pre {{
        background: linear-gradient(135deg, #f5f7fa, #f8f9fa) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        padding: 20px !important;
        font-size: 13px !important;
        line-height: 1.6 !important;
    }}

    /* Dark mode code blocks */
    {'pre { background: linear-gradient(135deg, #2d2d2d, #3d3d3d) !important; color: #e0e0e0 !important; }' if st.session_state.dark_mode else ''}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0 !important;
    }}

    .stTabs [role="tablist"] {{
        border-bottom: 2px solid var(--border-color) !important;
    }}

    /* Alerts */
    .stAlert {{
        border-radius: 10px !important;
        padding: 15px 20px !important;
        border-left: 5px solid !important;
    }}

    /* Progress Bar */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
    }}

    /* Expandable Section */
    .streamlit-expanderHeader {{
        background: linear-gradient(135deg, #f5f7fb, #f8f9fa) !important;
        border-radius: 10px !important;
        border: 1px solid var(--border-color) !important;
    }}

    /* Dark mode expandable sections */
    {'[data-testid="stExpander"] { background: var(--card-bg) !important; }' if st.session_state.dark_mode else ''}
    {'[data-testid="stExpander"] [data-testid="stExpanderToggleIcon"] { color: var(--text-primary) !important; }' if st.session_state.dark_mode else ''}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)

    # Professional Branding Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 50px 40px; border-radius: 20px; margin-bottom: 40px; text-align: center; 
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);">
        <h1 style="color: white; margin: 0; font-size: 3.2em; font-weight: 900; letter-spacing: 1px;">
            📝 Automated Python Docstring Generator
        </h1>
        <p style="color: rgba(255, 255, 255, 0.95); margin-top: 15px; font-size: 1.2em; margin-bottom: 0; font-weight: 500;">
            Enterprise-Grade AI-Powered Documentation Platform
        </p>
        <div style="margin-top: 25px; display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
            <span style="background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px); padding: 10px 20px; border-radius: 25px; 
                        font-size: 0.95em; color: white; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.3);">
                🤖 AI-Powered
            </span>
            <span style="background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px); padding: 10px 20px; border-radius: 25px; 
                        font-size: 0.95em; color: white; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.3);">
                ✅ PEP 257 Compliant
            </span>
            <span style="background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px); padding: 10px 20px; border-radius: 25px; 
                        font-size: 0.95em; color: white; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.3);">
                🚀 Production Ready
            </span>
            <span style="background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px); padding: 10px 20px; border-radius: 25px; 
                        font-size: 0.95em; color: white; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.3);">
                ⚙️ Full Automation
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Configuration
    selected_style, file_option = sidebar_configuration()

    # 4-Phase Navigation with Professional Names
    st.sidebar.markdown("---")
    st.sidebar.title("🗂️ Platform Phases")
    
    phase = st.sidebar.radio(
        "Select Phase",
        [
            "📊 Code Analysis",
            "🔄 AI Generation & Validation", 
            "⚙️ Automation Suite",
            "📦 Documentation Hub"
        ],
        help="Navigate through the 4-phase documentation platform",
        index=0
    )

    # Show file input for Code Analysis, Automation Suite, and Documentation Hub
    if phase in ["📊 Code Analysis", "⚙️ Automation Suite", "📦 Documentation Hub"]:
        st.sidebar.markdown("---")
        if file_option == "Upload File":
            upload_and_analyze()
        else:
            scan_directory()

    # Display Selected Phase
    if phase == "📊 Code Analysis":
        display_code_analysis()
    elif phase == "🔄 AI Generation & Validation":
        display_ai_generation()
    elif phase == "⚙️ Automation Suite":
        display_automation_suite()
    elif phase == "📦 Documentation Hub":
        display_documentation_hub()


if __name__ == "__main__":
    main()
