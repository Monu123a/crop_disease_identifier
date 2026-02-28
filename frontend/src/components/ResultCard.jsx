import React from 'react';
import './ResultCard.css';

const ResultCard = ({ result, onReset }) => {
    if (!result) return null;

    const {
        disease,
        severity,
        confidence,
        treatment,
        affectedCrops,
        prevention,
        nextSteps
    } = result;

    const getSeverityClass = (sev) => {
        switch (sev?.toLowerCase()) {
            case 'high': return 'sev-high';
            case 'medium': return 'sev-medium';
            case 'low': return 'sev-low';
            default: return '';
        }
    };

    return (
        <div className="result-card glass-panel">
            <div className="result-header">
                <div className="title-group">
                    <span className="label">Diagnosis</span>
                    <h2 className="disease-name">{disease}</h2>
                </div>
                <div className={`severity-badge ${getSeverityClass(severity)}`}>
                    {severity} Severity
                </div>
            </div>

            <div className="confidence-section">
                <div className="section-header">
                    <label>Confidence Level</label>
                    <span className="percentage">{confidence}%</span>
                </div>
                <div className="progress-track">
                    <div
                        className="progress-bar"
                        style={{ width: `${confidence}%` }}
                    ></div>
                </div>
            </div>

            <div className="info-grid">
                <div className="info-section">
                    <h4>📊 Affected Crops</h4>
                    <p>{affectedCrops || 'Various vegetable and fruit crops'}</p>
                </div>

                <div className="info-section">
                    <h4>🛡️ Prevention Tips</h4>
                    <p>{prevention || 'Maintain proper irrigation and ensure secondary airflow between plants.'}</p>
                </div>
            </div>

            <div className="treatment-card">
                <h4>💊 Recommended Treatment</h4>
                <p className="treatment-text">{treatment}</p>
            </div>

            <div className="next-steps">
                <h4>🚀 Next Steps</h4>
                <ul className="steps-list">
                    {nextSteps?.map((step, index) => (
                        <li key={index}>{step}</li>
                    )) || (
                            <>
                                <li>Isolate affected plants immediately</li>
                                <li>Consult with a local agriculture expert</li>
                                <li>Monitor surrounding crops for similar symptoms</li>
                            </>
                        )}
                </ul>
            </div>

            <button className="reset-btn" onClick={onReset}>
                Diagnose Another Leaf
            </button>
        </div>
    );
};

export default ResultCard;
