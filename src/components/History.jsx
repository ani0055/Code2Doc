import React, { useState, useEffect } from 'react';
import { getProjects, getProjectDetails, deleteProject, updateProjectName, exportDocumentationPDF, exportDocumentationDOCX } from '../services/api';
import ReactMarkdown from 'react-markdown';
import './History.css';

const History = ({ onBack }) => {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const data = await getProjects();
      setProjects(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleProjectClick = async (projectId) => {
    try {
      setLoading(true);
      const projectData = await getProjectDetails(projectId);
      setSelectedProject(projectData);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

   const handleEditClick = (project, e) => {
    e.stopPropagation();
    setEditingId(project.id);
    setEditName(project.name);
  };

  const handleSaveName = async (projectId, e) => {
    e.stopPropagation();
    if (editName.trim() === '') {
      alert('Project name cannot be empty');
      return;
    }

     try {
      await updateProjectName(projectId, editName);
      setProjects(projects.map(p => 
        p.id === projectId ? { ...p, name: editName } : p
      ));
      if (selectedProject?.id === projectId) {
        setSelectedProject({ ...selectedProject, name: editName });
      }
      setEditingId(null);
      alert('Project name updated!');
    } catch (err) {
      alert('Failed to update name: ' + err.message);
    }
  };

   const handleCancelEdit = (e) => {
    e.stopPropagation();
    setEditingId(null);
    setEditName('');
  };

  const handleDelete = async (projectId, e) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await deleteProject(projectId);
        setProjects(projects.filter(p => p.id !== projectId));
        if (selectedProject?.id === projectId) {
          setSelectedProject(null);
        }
        alert('Project deleted successfully');
      } catch (err) {
        alert('Failed to delete project: ' + err.message);
      }
    }
  };

  const handleExportPDF = async (docId) => {
    try {
      await exportDocumentationPDF(docId);
      alert('PDF downloaded successfully!');
    } catch (err) {
      alert('Failed to export PDF: ' + err.message);
    }
  };

  const handleExportDOCX = async (docId) => {
    try {
      await exportDocumentationDOCX(docId);
      alert('DOCX downloaded successfully!');
    } catch (err) {
      alert('Failed to export DOCX: ' + err.message);
    }
  };

  if (loading && projects.length === 0) {
    return (
      <div className="history-container">
        <div className="history-header">
          <h2>Documentation History</h2>
          <button onClick={onBack} className="btn-secondary">Back</button>
        </div>
        <div className="loading-message">Loading your projects...</div>
      </div>
    );
  }

  if (error && projects.length === 0) {
    return (
      <div className="history-container">
        <div className="history-header">
          <h2>Documentation History</h2>
          <button onClick={onBack} className="btn-secondary">Back</button>
        </div>
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <h2>Documentation History</h2>
        <button onClick={onBack} className="btn-secondary">Back</button>
      </div>

      <div className="history-content">
        {/* Projects List */}
        <div className="projects-list">
          <h3>Your Projects ({projects.length})</h3>
          {projects.length === 0 ? (
            <p className="no-projects">No projects yet. Analyze some code to get started!</p>
          ) : (
            <div className="project-cards">
                  
                  {projects.map(project => (
                    <div
                      key={project.id}
                      className={`project-card ${selectedProject?.id === project.id ? 'active' : ''}`}
                      onClick={() => !editingId && handleProjectClick(project.id)}
                    >
                      <div className="project-info">
                        {editingId === project.id ? (
                          <div className="edit-name-container" onClick={(e) => e.stopPropagation()}>
                            <input
                              type="text"
                              value={editName}
                              onChange={(e) => setEditName(e.target.value)}
                              className="edit-name-input"
                              autoFocus
                            />
                            <div className="edit-actions">
                              <button onClick={(e) => handleSaveName(project.id, e)} className="save-btn">
                                ✓
                              </button>
                              <button onClick={handleCancelEdit} className="cancel-btn">
                                ✕
                              </button>
                            </div>
                          </div>
                        ) : (
                          <>
                            <h4>{project.name}</h4>
                            <button
                              onClick={(e) => handleEditClick(project, e)}
                              className="edit-btn"
                              title="Edit project name"
                            >
                              ✏️
                            </button>
                          </>
                        )}
                        <span className="project-language">{project.language}</span>
                        <p className="project-date">
                          {new Date(project.created_at).toLocaleDateString()} at{' '}
                          {new Date(project.created_at).toLocaleTimeString()}
                        </p>
                      </div>
                      <button
                        onClick={(e) => handleDelete(project.id, e)}
                        className="delete-btn"
                        title="Delete project"
                      >
                        🗑️
                      </button>
                    </div>
                  ))}
            </div>
          )}
        </div>

        {/* Project Details */}
        <div className="project-details">
          {selectedProject ? (
            <>
              <div className="detail-header">
                <div>
                  <h3>{selectedProject.filename}</h3>
                  <span className="language-badge">{selectedProject.language}</span>
                </div>
              </div>

              {selectedProject.documentations && selectedProject.documentations.length > 0 ? (
                selectedProject.documentations.map((doc, index) => (
                  <div key={doc.id} className="documentation-section">
                    <div className="doc-header">
                      <h4>Documentation {selectedProject.documentations.length > 1 ? `#${index + 1}` : ''}</h4>
                      <div className="doc-actions">
                        <button
                          onClick={() => handleExportPDF(doc.id)}
                          className="btn-export"
                        >
                          Export PDF
                        </button>
                        <button
                          onClick={() => handleExportDOCX(doc.id)}
                          className="btn-export"
                        >
                          Export DOCX
                        </button>
                      </div>
                    </div>
                    
                    <div className="markdown-content">
                      <ReactMarkdown>{doc.markdown}</ReactMarkdown>
                    </div>

                    {doc.diagram && (
                      <div className="diagram-section">
                        <h4>Diagram</h4>
                        <pre className="diagram-code">{doc.diagram}</pre>
                        <p className="diagram-note">
                          Visualize at{' '}
                          <a href="https://mermaid.live" target="_blank" rel="noopener noreferrer">
                            mermaid.live
                          </a>
                        </p>
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <p>No documentation available for this project.</p>
              )}
            </>
          ) : (
            <div className="no-selection">
              <p>Select a project to view its documentation</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default History;