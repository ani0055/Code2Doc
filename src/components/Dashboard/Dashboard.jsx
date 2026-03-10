import React, { useState, useRef } from 'react';
import { analyzeCode, exportToPDF, exportToDOCX } from '../../services/api';
import History from '../History';
import FlowDiagram from '../FlowDiagram';
import Sidebar from './Sidebar';
import Header from './Header';
import ReactMarkdown from 'react-markdown';
import { toast } from 'react-toastify';
import './Dashboard.css';

const Dashboard = ({ user, onLogout, toggleTheme, isDarkMode }) => {
    const [step, setStep] = useState('upload');
    const [view, setView] = useState('main'); // 'main' or 'history'
    const [code, setCode] = useState('');
    const [fileName, setFileName] = useState('');
    const [needsDiagram, setNeedsDiagram] = useState(false);
    const [documentation, setDocumentation] = useState(null);
    const [loading, setLoading] = useState(false);
    const [pageError, setPageError] = useState(null);
    const diagramRef = useRef(null);

    const handleCodeSubmit = (submittedCode, submittedFileName) => {
        if (submittedCode.trim() === '') {
            setPageError('Error: Code cannot be empty.');
            return;
        }
        setPageError(null);
        setCode(submittedCode);
        let detectedFileName = submittedFileName;

        if (!detectedFileName) {
            const codeLower = submittedCode.toLowerCase();
            if (codeLower.includes('import java') || codeLower.includes('public class')) {
                detectedFileName = 'file.java';
            } else if (codeLower.includes('console.log') || codeLower.includes('function(') || codeLower.includes('=>')) {
                detectedFileName = 'file.js';
            } else if (codeLower.includes('def ') || codeLower.includes('import ') || codeLower.includes('print(')) {
                detectedFileName = 'file.py';
            } else {
                detectedFileName = 'file.txt';
            }
        }

        setFileName(detectedFileName);
        setStep('askDiagram');
    };

    const handleDiagramChoice = async (choice) => {
        setNeedsDiagram(choice);
        setStep('generating');
        setLoading(true);
        setPageError(null);

        try {
            const result = await analyzeCode(code, fileName, choice);
            setDocumentation({
                markdown: result.markdown,
                diagram: result.diagram,
                language: result.language,
                structure: result.structure,
                metrics: result.metrics
            });
            setStep('result');
        } catch (error) {
            console.error('Analysis error:', error);
            const errorMessage = error.response?.data?.detail || error.message || 'Failed to analyze code';
            setPageError('Analysis failed: ' + errorMessage);
            setStep('upload');
        } finally {
            setLoading(false);
        }
    };

    const handleExport = async (format) => {
        try {
            const baseName = fileName.split('.')[0] || 'documentation';
            let diagramImage = null;

            if (documentation.diagram && diagramRef.current) {
                try {
                    diagramImage = await diagramRef.current.exportAsImage();
                } catch (err) {
                    console.error('Failed to capture diagram:', err);
                }
            }

            if (format === 'PDF') {
                await exportToPDF(documentation.markdown, baseName, diagramImage);
                toast.success('PDF downloaded successfully!');
            } else if (format === 'DOCX') {
                await exportToDOCX(documentation.markdown, baseName, diagramImage);
                toast.success('DOCX downloaded successfully!');
            } else {
                const content = documentation.markdown;
                const blob = new Blob([content], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${baseName}.${format.toLowerCase()}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                toast.success(`Documentation downloaded as ${format}`);
            }
        } catch (error) {
            setPageError('Export failed: ' + error.message);
            alert('Export failed: ' + error.message);
        }
    };

    const handleReset = () => {
        setCode('');
        setFileName('');
        setDocumentation(null);
        setStep('upload');
        setPageError(null);
    };

    return (
        <div className="dashboard-layout">
            <Sidebar currentView={view} onViewChange={setView} />

            <div className="dashboard-main">
                <Header user={user} onLogout={onLogout} toggleTheme={toggleTheme} isDarkMode={isDarkMode} />

                <main className="dashboard-content">
                    {pageError && <div className="modern-error-message glass-panel">{pageError}</div>}

                    {view === 'history' ? (
                        <div className="glass-panel history-container-modern">
                            <History onBack={() => setView('main')} />
                        </div>
                    ) : (
                        <div className="main-flow-container">
                            {step === 'upload' && (
                                <UploadStep onSubmit={handleCodeSubmit} />
                            )}

                            {step === 'askDiagram' && (
                                <div className="glass-panel center-step-card">
                                    <h2>Generate Diagrams?</h2>
                                    <p>Would you like to generate a visual Workflow diagram for your code?</p>
                                    <div className="modern-button-group">
                                        <button onClick={() => handleDiagramChoice(true)} className="btn-modern-primary">
                                            Yes, Generate Diagram
                                        </button>
                                        <button onClick={() => handleDiagramChoice(false)} className="btn-modern-secondary">
                                            No, Thanks
                                        </button>
                                    </div>
                                </div>
                            )}

                            {step === 'generating' && (
                                <div className="glass-panel center-step-card">
                                    <h2>Analyzing Your Code...</h2>
                                    <div className="modern-loader"></div>
                                    <p className="loading-text">Extracting logic and structuring documentation...</p>
                                </div>
                            )}

                            {step === 'result' && documentation && (
                                <div className="dashboard-bento-grid">
                                    {/* Action Header spanning full width */}
                                    <div className="bento-item glass-panel action-bar">
                                        <h2>Analysis Complete</h2>
                                        <div className="action-buttons">
                                            <button onClick={() => handleExport('PDF')} className="btn-modern-secondary btn-sm">PDF</button>
                                            <button onClick={() => handleExport('DOCX')} className="btn-modern-secondary btn-sm">DOCX</button>
                                            <button onClick={() => handleExport('MD')} className="btn-modern-secondary btn-sm">MD</button>
                                            <button onClick={handleReset} className="btn-modern-primary btn-sm">Analyze New</button>
                                        </div>
                                    </div>

                                    {/* Overview Metrics side panel */}
                                    <div className="bento-item glass-panel overview-metrics">
                                        <h3>Overview</h3>
                                        <div className="metric-list">
                                            <div className="metric-row">
                                                <span>Language</span>
                                                <strong>{documentation.language || 'N/A'}</strong>
                                            </div>
                                            <div className="metric-row">
                                                <span>Functions</span>
                                                <strong>{documentation.structure?.functions?.length || 0}</strong>
                                            </div>
                                            <div className="metric-row">
                                                <span>Classes</span>
                                                <strong>{documentation.structure?.classes?.length || 0}</strong>
                                            </div>
                                            {documentation.metrics && (
                                                <>
                                                    <div className="metric-row">
                                                        <span>LoC</span>
                                                        <strong>{documentation.metrics.lines_of_code}</strong>
                                                    </div>
                                                    <div className="metric-row">
                                                        <span>Maintainability</span>
                                                        <strong className={documentation.metrics.maintainability_index >= 50 ? 'text-success' : 'text-danger'}>
                                                            {documentation.metrics.maintainability_index || 0}
                                                        </strong>
                                                    </div>
                                                </>
                                            )}
                                        </div>

                                        {documentation.metrics?.suggestions?.length > 0 && (
                                            <div className="suggestions-mini">
                                                <h4>Top Tips</h4>
                                                <ul>
                                                    {documentation.metrics.suggestions.slice(0, 3).map((s, i) => <li key={i}>{s}</li>)}
                                                </ul>
                                            </div>
                                        )}
                                    </div>

                                    {/* Main Documentation Area */}
                                    <div className="bento-item glass-panel main-markdown">
                                        <h3>Documentation</h3>
                                        <div className="markdown-modern-content">
                                            <ReactMarkdown>{documentation.markdown}</ReactMarkdown>
                                        </div>
                                    </div>

                                    {/* Flow Diagram Area */}
                                    {documentation.diagram && (
                                        <div className="bento-item glass-panel diagram-area">
                                            <h3>Code Flow</h3>
                                            <FlowDiagram ref={diagramRef} diagramData={documentation.diagram} />
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    )}
                </main>
            </div>
        </div>
    );
};

const UploadStep = ({ onSubmit }) => {
    const [code, setCode] = useState('');
    const [fileName, setFileName] = useState('');

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFileName(file.name);
            const reader = new FileReader();
            reader.onload = (event) => {
                setCode(event.target.result);
            };
            reader.readAsText(file);
        }
    };

    const handleSubmit = () => {
        if (code.trim() === '') {
            alert('Please upload a file or paste code');
            return;
        }
        onSubmit(code, fileName);
    };

    return (
        <div className="glass-panel upload-card modern-upload">
            <h2>Upload Source Code</h2>
            <p>Paste your snippet or upload a file (.py, .js, .jsx, .java)</p>

            <div className="file-drop-area">
                <label htmlFor="file-upload" className="file-label">
                    <span className="upload-icon">📁</span>
                    {fileName || 'Choose File...'}
                </label>
                <input
                    id="file-upload"
                    type="file"
                    onChange={handleFileChange}
                    accept=".py,.js,.jsx,.ts,.tsx,.java"
                    className="hidden-input"
                />
            </div>

            <div className="code-editor-container">
                <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="...or paste your target code here."
                    className="modern-code-textarea"
                />
            </div>

            <button onClick={handleSubmit} className="btn-modern-primary w-full mt-4">
                Generate Analysis
            </button>
        </div>
    );
};

export default Dashboard;
