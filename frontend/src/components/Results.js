import React, { useState } from 'react';
import { motion } from 'framer-motion';
import AdvancedAnalysis from './AdvancedAnalysis';

const ConfusionMatrix = ({ matrix, title }) => {
  return (
    <div className="confusion-matrix">
      <h4>{title}</h4>
      <div className="matrix-grid">
        <div className="matrix-labels">
          <div className="label-corner"></div>
          <div className="label-top">Predicted Rejected</div>
          <div className="label-top">Predicted Accepted</div>
        </div>
        <div className="matrix-row">
          <div className="label-left">Actual Rejected</div>
          <div className="matrix-cell tn">{matrix[0][0]}</div>
          <div className="matrix-cell fp">{matrix[0][1]}</div>
        </div>
        <div className="matrix-row">
          <div className="label-left">Actual Accepted</div>
          <div className="matrix-cell fn">{matrix[1][0]}</div>
          <div className="matrix-cell tp">{matrix[1][1]}</div>
        </div>
      </div>
    </div>
  );
};

const MetricsCard = ({ model, metrics }) => {
  return (
    <motion.div
      className="metrics-card-horizontal"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="model-header-horizontal">
        <h4>{model}</h4>
      </div>
      <div className="model-content-horizontal">
        <div className="metrics-left">
          <div className="metric-item">
            <span className="metric-label">Accuracy</span>
            <span className="metric-value">{(metrics.accuracy * 100).toFixed(1)}%</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Precision</span>
            <span className="metric-value">{(metrics.precision * 100).toFixed(1)}%</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Recall</span>
            <span className="metric-value">{(metrics.recall * 100).toFixed(1)}%</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">F1 Score</span>
            <span className="metric-value">{(metrics.f1_score * 100).toFixed(1)}%</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">AUC Score</span>
            <span className="metric-value">{(metrics.auc_score * 100).toFixed(1)}%</span>
          </div>
        </div>
        <div className="confusion-right">
          <ConfusionMatrix matrix={metrics.confusion_matrix} title="Confusion Matrix" />
        </div>
      </div>
    </motion.div>
  );
};

const Results = ({ data, onReset }) => {
  const [showAnalysis, setShowAnalysis] = useState(false);

  return (
    <motion.div
      className="results-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
    >
      <div className="results-card">
        <div className="results-header">
          <h2>Analysis Complete</h2>
          <div className="header-buttons">
            <button onClick={() => setShowAnalysis(!showAnalysis)} className="analysis-btn">
              {showAnalysis ? 'Hide' : 'Show'} ML Analysis
            </button>
            <button onClick={onReset} className="reset-btn">
              Upload Another
            </button>
          </div>
        </div>

        <div className="info-section">
          <div className="info-item">
            <strong>Email:</strong> {data.email || 'Not found'}
          </div>
          <div className="info-item">
            <strong>Phone:</strong> {data.phone || 'Not found'}
          </div>
          <div className="info-item">
            <strong>File:</strong> {data.filename}
          </div>
          {data.skills && data.skills.length > 0 && (
            <div className="info-item skills-item">
              <strong>Detected Skills:</strong>
              <div className="skills-tags">
                {data.skills.map((skill, idx) => (
                  <span key={idx} className="skill-tag">{skill}</span>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="jobs-section">
          <h3>Recommended Jobs</h3>
          {data.jobs && data.jobs.map((job, index) => (
            <motion.div
              key={index}
              className="job-card"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="job-header">
                <div className="job-title">{job.title}</div>
                <div className="match-badge">{job.match}% Match</div>
              </div>
              <div className="job-company">{job.company}</div>
              <div className="job-description">{job.description}</div>
              {job.matching_skills && job.matching_skills.length > 0 && (
                <div className="matching-skills">
                  <strong>Matching Skills:</strong>
                  <div className="skills-tags">
                    {job.matching_skills.map((skill, idx) => (
                      <span key={idx} className="skill-tag match">{skill}</span>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </div>

      {showAnalysis && data.ml_analysis && (
        <motion.div
          className="analysis-section"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
        >
          <h2 className="analysis-title">Machine Learning Model Analysis</h2>
          
          <div className="models-vertical">
            <MetricsCard 
              model="Decision Tree" 
              metrics={data.ml_analysis.decision_tree}
            />
            <MetricsCard 
              model="Logistic Regression" 
              metrics={data.ml_analysis.logistic_regression}
            />
            <MetricsCard 
              model="Random Forest" 
              metrics={data.ml_analysis.random_forest}
            />
          </div>

          <AdvancedAnalysis data={data.ml_analysis} />
          
          <div className="best-model">
            <h3>Best Performing Model: Random Forest</h3>
            <p>Based on accuracy and F1 score metrics</p>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default Results;
