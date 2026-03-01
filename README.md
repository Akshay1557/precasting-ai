# Precasting-AI

## CREATECH 2026 Competition Submission

### AI-Based Concrete Demoulding Cycle Time Optimizer

**Live Application:**\
https://precasting-ai.streamlit.app/

------------------------------------------------------------------------

# Executive Summary

Precasting-AI is an AI-driven industrial optimization system developed
for CREATECH 2026.\
The system minimizes concrete demoulding cycle time using a Hybrid
Physics + Machine Learning model.

It enables precast industries to:

-   Reduce production cycle time\
-   Lower curing energy costs\
-   Optimize operational decisions\
-   Improve plant efficiency using AI

This solution bridges Mechanical Engineering principles with Artificial
Intelligence to create a smart manufacturing optimization tool.

------------------------------------------------------------------------

# Technical Innovation

## Physics-Based Hydration Model

Implements:

-   Nurse-Saul Maturity Concept\
-   Cement hydration kinetics\
-   Temperature acceleration factors\
-   Environmental correction (humidity + wind impact)

Ensures scientifically reliable predictions grounded in engineering
fundamentals.

------------------------------------------------------------------------

## Machine Learning Model

-   RandomForestRegressor\
-   Trained on strength vs time dataset\
-   Captures nonlinear curing behavior\
-   Improves prediction accuracy under varying conditions

------------------------------------------------------------------------

## Hybrid Intelligence Model

Final Strength Prediction:

Final Strength =\
0.6 × Physics Model + 0.4 × ML Model

This hybrid approach provides:

✔ Engineering reliability\
✔ Data-driven adaptability\
✔ Real-world robustness

------------------------------------------------------------------------

# Live Industrial Simulation

The deployed Streamlit application dynamically accepts:

-   Required demoulding strength (MPa)\
-   Average curing temperature (°C)\
-   Relative humidity\
-   Wind speed\
-   Mix design\
-   Curing method

The system calculates in real-time:

-   Strength development curve\
-   Optimal demoulding time\
-   Estimated curing cost\
-   Best mix-curing strategy

All results are computed live inside the cloud-hosted application.

------------------------------------------------------------------------

# Optimization Strategy

Each mix + curing combination is evaluated based on:

-   Cycle Time\
-   Operational Cost

Scoring Model:

Score =\
0.6 × Time_Normalized + 0.4 × Cost_Normalized

Lowest score represents the optimal industrial strategy.

------------------------------------------------------------------------

# CREATECH 2026 Impact Alignment

## Industry 4.0 Integration

-   Smart decision system\
-   AI-assisted manufacturing\
-   Data-driven process optimization

## Sustainability Impact

-   Reduced energy consumption\
-   Lower steam curing usage\
-   Optimized material performance

## Scalability

-   Can integrate IoT temperature sensors\
-   Expandable cement type database\
-   Cloud-ready architecture

------------------------------------------------------------------------

# Technology Stack

-   Python\
-   Streamlit\
-   NumPy\
-   Pandas\
-   Matplotlib\
-   Scikit-learn

------------------------------------------------------------------------

# Key Features

-   Real-time strength prediction\
-   Hybrid AI + Engineering model\
-   Multi-scenario evaluation\
-   Cost comparison visualization\
-   Strength growth graph\
-   Cloud deployment

------------------------------------------------------------------------

# Local Setup

git clone https://github.com/your-username/precasting-ai.git\
cd precasting-ai\
pip install -r requirements.txt\
streamlit run streamlit_app.py

------------------------------------------------------------------------

# Deployment

Hosted on Streamlit Community Cloud

Live URL:\
https://precasting-ai.streamlit.app/


------------------------------------------------------------------------

# CREATECH 2026 Submission Note

This project demonstrates the integration of core mechanical engineering
principles with artificial intelligence to optimize industrial concrete
manufacturing processes in real time.

Designed for smart manufacturing, sustainability, and Industry 4.0
applications.
