import React from 'react';
import { motion } from 'framer-motion';

const ROCCurve = ({ data }) => {
  const models = ['decision_tree', 'logistic_regression', 'random_forest'];
  const colors = ['#ef4444', '#3b82f6', '#22c55e'];
  const names = ['Decision Tree', 'Logistic Regression', 'Random Forest'];
  
  const svgWidth = 400;
  const svgHeight = 400;
  const padding = 40;
  
  const scaleX = (x) => padding + (x * (svgWidth - 2 * padding));
  const scaleY = (y) => svgHeight - padding - (y * (svgHeight - 2 * padding));
  
  return (
    <div className="roc-curve-container">
      <h4>ROC Curve Comparison</h4>
      <svg width={svgWidth} height={svgHeight} className="roc-svg">
        <line 
          x1={padding} y1={svgHeight - padding} 
          x2={svgWidth - padding} y2={svgHeight - padding} 
          stroke="#4b5563" strokeWidth="2"
        />
        <line 
          x1={padding} y1={padding} 
          x2={padding} y2={svgHeight - padding} 
          stroke="#4b5563" strokeWidth="2"
        />
        
        <line 
          x1={padding} y1={svgHeight - padding} 
          x2={svgWidth - padding} y2={padding} 
          stroke="#6b7280" strokeWidth="1" strokeDasharray="5,5"
        />
        
        <text x={svgWidth / 2} y={svgHeight - 10} fill="#9ca3af" fontSize="12" textAnchor="middle">
          False Positive Rate
        </text>
        <text x="15" y={svgHeight / 2} fill="#9ca3af" fontSize="12" textAnchor="middle" transform={`rotate(-90, 15, ${svgHeight / 2})`}>
          True Positive Rate
        </text>
        
        {models.map((model, idx) => {
          const roc = data[model].roc_curve;
          const points = roc.fpr.map((fpr, i) => ({
            x: scaleX(fpr),
            y: scaleY(roc.tpr[i])
          }));
          
          const pathData = points.map((p, i) => 
            `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`
          ).join(' ');
          
          return (
            <g key={model}>
              <path 
                d={pathData} 
                fill="none" 
                stroke={colors[idx]} 
                strokeWidth="3"
              />
              {points.map((p, i) => (
                <circle 
                  key={i} 
                  cx={p.x} 
                  cy={p.y} 
                  r="4" 
                  fill={colors[idx]}
                />
              ))}
            </g>
          );
        })}
      </svg>
      
      <div className="roc-legend">
        {models.map((model, idx) => (
          <div key={model} className="legend-item">
            <div className="legend-color" style={{ backgroundColor: colors[idx] }}></div>
            <span>{names[idx]} (AUC: {data[model].auc_score.toFixed(3)})</span>
          </div>
        ))}
      </div>
    </div>
  );
};

const FeatureImportance = ({ features }) => {
  const maxImportance = Math.max(...features.map(f => f.importance));
  
  return (
    <div className="feature-importance">
      <h4>Feature Importance</h4>
      <div className="features-list">
        {features.map((feature, idx) => (
          <motion.div 
            key={idx} 
            className="feature-bar-container"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <div className="feature-label">{feature.feature}</div>
            <div className="feature-bar-wrapper">
              <motion.div 
                className="feature-bar"
                initial={{ width: 0 }}
                animate={{ width: `${(feature.importance / maxImportance) * 100}%` }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
              >
                <span className="feature-value">{(feature.importance * 100).toFixed(1)}%</span>
              </motion.div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

const CrossValidation = ({ cvData }) => {
  const models = Object.keys(cvData);
  const modelNames = {
    'decision_tree': 'Decision Tree',
    'logistic_regression': 'Logistic Regression',
    'random_forest': 'Random Forest'
  };
  
  return (
    <div className="cross-validation">
      <h4>Cross-Validation Scores (5-Fold)</h4>
      <div className="cv-grid">
        {models.map((model) => {
          const scores = cvData[model];
          const mean = (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(3);
          const std = Math.sqrt(
            scores.reduce((sum, score) => sum + Math.pow(score - mean, 2), 0) / scores.length
          ).toFixed(3);
          
          return (
            <div key={model} className="cv-card">
              <h5>{modelNames[model]}</h5>
              <div className="cv-scores">
                {scores.map((score, idx) => (
                  <div key={idx} className="cv-score-item">
                    <span className="fold-label">Fold {idx + 1}</span>
                    <span className="fold-score">{(score * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
              <div className="cv-stats">
                <div className="stat-item">
                  <span className="stat-label">Mean:</span>
                  <span className="stat-value">{(mean * 100).toFixed(1)}%</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Std Dev:</span>
                  <span className="stat-value">{(std * 100).toFixed(1)}%</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const ModelComparison = ({ data }) => {
  const models = ['decision_tree', 'logistic_regression', 'random_forest'];
  const modelNames = ['Decision Tree', 'Logistic Regression', 'Random Forest'];
  const metrics = ['accuracy', 'precision', 'recall', 'f1_score'];
  const metricNames = ['Accuracy', 'Precision', 'Recall', 'F1 Score'];
  const colors = ['#ef4444', '#3b82f6', '#22c55e'];
  
  return (
    <div className="model-comparison-chart">
      <h4>Model Performance Comparison</h4>
      <div className="comparison-cards-grid">
        {metrics.map((metric, metricIdx) => (
          <motion.div 
            key={metric} 
            className="comparison-metric-card"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: metricIdx * 0.1 }}
          >
            <div className="comparison-metric-title">{metricNames[metricIdx]}</div>
            <div className="comparison-bars-vertical">
              {models.map((model, modelIdx) => {
                const value = data[model][metric];
                return (
                  <div key={model} className="comparison-bar-item">
                    <div className="comparison-model-name">{modelNames[modelIdx]}</div>
                    <div className="comparison-bar-track">
                      <motion.div 
                        className="comparison-bar-fill"
                        style={{ backgroundColor: colors[modelIdx] }}
                        initial={{ width: 0 }}
                        animate={{ width: `${value * 100}%` }}
                        transition={{ duration: 0.5, delay: metricIdx * 0.1 + modelIdx * 0.05 }}
                      >
                        <span className="comparison-bar-text">{(value * 100).toFixed(1)}%</span>
                      </motion.div>
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

const ClassificationReport = ({ data }) => {
  const models = ['decision_tree', 'logistic_regression', 'random_forest'];
  const modelNames = ['Decision Tree', 'Logistic Regression', 'Random Forest'];
  
  return (
    <div className="classification-report">
      <h4>Detailed Classification Report</h4>
      <div className="report-grid">
        {models.map((model, idx) => (
          <div key={model} className="report-card">
            <h5>{modelNames[idx]}</h5>
            <table className="report-table">
              <thead>
                <tr>
                  <th>Class</th>
                  <th>Precision</th>
                  <th>Recall</th>
                  <th>F1-Score</th>
                  <th>Support</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Rejected</td>
                  <td>{data[model].precision.toFixed(2)}</td>
                  <td>{data[model].recall.toFixed(2)}</td>
                  <td>{data[model].f1_score.toFixed(2)}</td>
                  <td>{data[model].support.rejected}</td>
                </tr>
                <tr>
                  <td>Accepted</td>
                  <td>{data[model].precision.toFixed(2)}</td>
                  <td>{data[model].recall.toFixed(2)}</td>
                  <td>{data[model].f1_score.toFixed(2)}</td>
                  <td>{data[model].support.accepted}</td>
                </tr>
                <tr className="report-total">
                  <td>Accuracy</td>
                  <td colSpan="3">{data[model].accuracy.toFixed(2)}</td>
                  <td>{data[model].support.rejected + data[model].support.accepted}</td>
                </tr>
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
};

const AdvancedAnalysis = ({ data }) => {
  return (
    <div className="advanced-analysis">
      <div className="analysis-grid">
        <div className="analysis-item full-width">
          <FeatureImportance features={data.feature_importance} />
        </div>
        
        <div className="analysis-item full-width">
          <ROCCurve data={data} />
        </div>
        
        <div className="analysis-item full-width">
          <ModelComparison data={data} />
        </div>
        
        <div className="analysis-item full-width">
          <CrossValidation cvData={data.cross_validation} />
        </div>
        
        <div className="analysis-item full-width">
          <ClassificationReport data={data} />
        </div>
      </div>
    </div>
  );
};

export default AdvancedAnalysis;
