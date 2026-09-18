# Project Limitations

This system is designed as an educational tool and industrial-training project. The following limitations should be noted:

1. **Synthetic Dataset**: The student data (`sample_students.csv`) is programmatically generated. The correlations and distributions may not fully mimic real-world clinical or educational environments. Model performance should not be interpreted as real-world predictive validity.
2. **Limited Feature Set**: The predictions are based strictly on a subset of academic metrics (attendance, marks, study hours). The model does not account for qualitative, psychological, or socioeconomic factors.
3. **Rule-Based Risk Engine**: The risk thresholds (e.g., < 75% attendance) are manually defined constraints rather than statistically proven causation mechanisms.
4. **Data Quality Dependency**: Model performance relies heavily on accurate data entry. 
5. **No Production Deployment**: This is a local desktop application utilizing SQLite. It is not designed to support high-concurrency cloud environments or remote multi-user synchronization.
6. **Assistive Tool Only**: Predictions should support—not replace—human academic intervention decisions.
