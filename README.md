# Adaptive Control under Nonlinear Feedback

This project studies optimal decision-making in a nonlinear system where continuous input becomes counterproductive due to state-dependent feedback (thermal blooming).

## Key Idea
Continuous strategies maximize instantaneous input, but fail under nonlinear degradation. An adaptive policy regulates input based on system state, improving performance under uncertainty.

## Results
- Continuous strategy performs well at short range
- Adaptive strategy dominates in high nonlinearity regimes
- Clear regime transition observed

## Files
- model.py → core simulation
- analysis.py → generates all plots

## Run
python analysis.py
# <img width="580" height="455" alt="image" src="https://github.com/user-attachments/assets/2cf34076-6b10-4946-9a0d-d6365d9ceac7" />
 #   <img width="562" height="455" alt="image" src="https://github.com/user-attachments/assets/8c8c637b-17e0-45a0-84ce-198f754dc733" />
