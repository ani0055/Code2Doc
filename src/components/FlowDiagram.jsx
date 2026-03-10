import React, { useEffect, useRef, useState, forwardRef, useImperativeHandle } from 'react';
import { Network } from 'vis-network';
import html2canvas from 'html2canvas';

const FlowDiagram = forwardRef(({ diagramData }, ref) => {
  const containerRef = useRef(null);
  const [error, setError] = useState(null);
  const [parsedData, setParsedData] = useState(null);
  const networkRef = useRef(null);

  // Expose exportAsImage function to parent component
  useImperativeHandle(ref, () => ({
    exportAsImage: async () => {
      if (!containerRef.current) {
        console.error('Container not available for export');
        return null;
      }

      try {
        // Wait for diagram to fully render
        await new Promise(resolve => setTimeout(resolve, 500));

        const canvas = await html2canvas(containerRef.current, {
          backgroundColor: '#ffffff',
          scale: 2,
          logging: false,
          useCORS: true,
          allowTaint: true
        });

        return canvas.toDataURL('image/png');
      } catch (error) {
        console.error('Error exporting diagram:', error);
        return null;
      }
    },
    // Also expose the parsed data if needed
    getDiagramData: () => parsedData
  }));

  useEffect(() => {
    if (diagramData) {
      parseAndRender();
    }

    return () => {
      if (networkRef.current) {
        networkRef.current.destroy();
        networkRef.current = null;
      }
    };
  }, [diagramData]);

  const parseAndRender = () => {
    try {
      setError(null);

      let data;
      let cleaned = diagramData.trim();

      // Remove markdown code fences
      cleaned = cleaned.replace(/```json\s*/gi, '');
      cleaned = cleaned.replace(/```\s*$/g, '');
      cleaned = cleaned.replace(/^```\s*/g, '');

      // Extract JSON from text
      const jsonMatch = cleaned.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        cleaned = jsonMatch[0];
      }

      try {
        data = JSON.parse(cleaned);
      } catch (parseError) {
        console.warn('JSON parsing failed, using fallback');
        data = createFallbackDiagram();
      }

      setParsedData(data);
      renderDiagram(data);

    } catch (err) {
      console.error('Diagram error:', err);
      setError('Could not parse diagram data. Using fallback visualization.');
      renderFallbackDiagram();
    }
  };

  const createFallbackDiagram = () => {
    return {
      nodes: [
        { id: 'start', label: 'Code Entry Point', color: '#4CAF50' },
        { id: 'main', label: 'Main Logic', color: '#2196F3' },
        { id: 'end', label: 'End', color: '#F44336' }
      ],
      edges: [
        { from: 'start', to: 'main', label: 'executes' },
        { from: 'main', to: 'end', label: 'completes' }
      ]
    };
  };

  const renderDiagram = (data) => {
    if (!containerRef.current || !data.nodes || !data.edges) {
      renderFallbackDiagram();
      return;
    }

    const nodes = data.nodes.map(node => ({
      id: node.id,
      label: node.label,
      color: {
        background: node.color || '#2196F3',
        border: '#1976D2',
        highlight: {
          background: '#42A5F5',
          border: '#1565C0'
        }
      },
      font: { color: '#ffffff', size: 14 },
      shape: 'box',
      margin: 10
    }));

    const edges = data.edges.map((edge, index) => ({
      id: `edge-${index}`,
      from: edge.from,
      to: edge.to,
      label: edge.label || '',
      arrows: 'to',
      color: { color: '#666666' },
      font: { size: 12, color: '#666666', align: 'middle' }
    }));

    const graphData = { nodes, edges };

    const options = {
      layout: {
        hierarchical: {
          direction: 'UD',
          sortMethod: 'directed',
          levelSeparation: 150,
          nodeSpacing: 200
        }
      },
      physics: {
        enabled: false
      },
      edges: {
        smooth: {
          type: 'cubicBezier',
          forceDirection: 'vertical'
        }
      },
      interaction: {
        dragNodes: true,
        dragView: true,
        zoomView: true
      }
    };

    if (networkRef.current) {
      networkRef.current.destroy();
    }

    networkRef.current = new Network(containerRef.current, graphData, options);
  };

  const renderFallbackDiagram = () => {
    const fallbackData = createFallbackDiagram();
    renderDiagram(fallbackData);
  };

  const downloadAsImage = async () => {
    if (!containerRef.current) return;

    try {
      const canvas = await html2canvas(containerRef.current, {
        backgroundColor: '#ffffff',
        scale: 2,
        logging: false,
        useCORS: true
      });

      const link = document.createElement('a');
      link.download = `flow-diagram-${Date.now()}.png`;
      link.href = canvas.toDataURL('image/png');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Export failed:', error);
      alert('Failed to export diagram: ' + error.message);
    }
  };

  const copyJSON = () => {
    if (!parsedData) return;

    const jsonString = JSON.stringify(parsedData, null, 2);
    navigator.clipboard.writeText(jsonString)
      .then(() => alert('Diagram data copied to clipboard!'))
      .catch(() => alert('Failed to copy'));
  };

  return (
    <div className="glass-panel" style={{ padding: '20px', borderRadius: '12px' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '16px',
        paddingBottom: '16px',
        borderBottom: '1px solid var(--border-color)'
      }}>
        <h4 style={{ margin: 0, fontSize: '18px' }}>
          📊 Code Flow Diagram
        </h4>
        <div style={{ display: 'flex', gap: '8px' }}>
          {parsedData && (
            <button onClick={copyJSON} className="btn-modern-secondary btn-sm" title="Copy JSON">
              📋 Copy Data
            </button>
          )}
          <button onClick={parseAndRender} className="btn-modern-secondary btn-sm" title="Refresh">
            🔄 Refresh
          </button>
          <button onClick={downloadAsImage} className="btn-modern-primary btn-sm" title="Download as Image">
            📥 Download PNG
          </button>
        </div>
      </div>

      {error && (
        <div className="modern-error-message glass-panel" style={{ padding: '12px', marginBottom: '16px' }}>
          ⚠️ {error}
        </div>
      )}

      <div
        ref={containerRef}
        style={{
          height: '500px',
          border: '1px solid var(--border-color)',
          borderRadius: '12px',
          backgroundColor: '#ffffff' /* explicitly white for visibility of vis.js edges */
        }}
      />

      <div className="glass-panel" style={{
        display: 'flex',
        gap: '16px',
        marginTop: '16px',
        padding: '12px',
        border: '1px solid var(--border-color)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '16px', height: '16px', backgroundColor: '#4CAF50', borderRadius: '3px' }}></span>
          <span style={{ fontSize: '14px', color: 'var(--text-color)' }}>Entry Point</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '16px', height: '16px', backgroundColor: '#2196F3', borderRadius: '3px' }}></span>
          <span style={{ fontSize: '14px', color: 'var(--text-color)' }}>Functions</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '16px', height: '16px', backgroundColor: '#FF9800', borderRadius: '3px' }}></span>
          <span style={{ fontSize: '14px', color: 'var(--text-color)' }}>Classes</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '16px', height: '16px', backgroundColor: '#F44336', borderRadius: '3px' }}></span>
          <span style={{ fontSize: '14px', color: 'var(--text-color)' }}>End Point</span>
        </div>
      </div>

      <div style={{
        marginTop: '12px',
        padding: '12px',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        border: '1px solid rgba(59, 130, 246, 0.2)',
        borderRadius: '6px',
        fontSize: '14px',
        color: '#60a5fa'
      }}>
        💡 <strong>Tip:</strong> Drag nodes to reposition, zoom with mouse wheel, and pan by dragging the background
      </div>
    </div>
  );
});

FlowDiagram.displayName = 'FlowDiagram';

export default FlowDiagram;