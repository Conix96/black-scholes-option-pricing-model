# Black-Scholes Option Pricing Model 📊

An interactive web application built with Streamlit that implements the Black-Scholes option pricing model. This tool helps traders and financial analysts calculate option prices and analyze various option trading metrics through an intuitive interface.

![Demo](./resources/demo.mp4)

## 🚀 Features

- **Real-time Option Price Calculation**
  - Calculate call and put option prices
  - Interactive parameter adjustment
  - Visual price display

- **Greek Parameters Analysis**
  - Delta: Measure of option price sensitivity to underlying price changes
  - Gamma: Rate of change in Delta
  - Theta: Time decay measurement
  - Vega: Sensitivity to volatility changes
  - Rho: Sensitivity to interest rate changes

- **Advanced Visualizations**
  - Price sensitivity heatmaps
  - Profit/Loss analysis charts
  - Interactive plots with Plotly

- **Data Export**
  - Download analysis results as CSV
  - Comprehensive pricing data
  - PnL calculations

## 🛠️ Technology Stack

- **Python 3.8+**
- **Key Libraries:**
  - Streamlit: Web application framework
  - NumPy: Numerical computations
  - Pandas: Data manipulation
  - Plotly: Interactive visualizations
  - Matplotlib & Seaborn: Static visualizations
  - SciPy: Statistical computations

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Conix96/black-scholes-option-pricing-model.git
   cd black-scholes-option-pricing-model
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Input parameters in the sidebar:
   - Current asset price
   - Strike price
   - Time to maturity
   - Volatility
   - Risk-free rate

4. Analyze results through:
   - Option prices display
   - Greeks analysis
   - Interactive heatmaps
   - PnL charts

## 📊 Project Structure

```
black-scholes-option-pricing-model/
├── app.py                 # Main Streamlit application
├── black_scholes_model.py # Core Black-Scholes implementation
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
└── tests/                # Unit tests
```

## 🧮 Mathematical Foundation

The Black-Scholes model uses the following formula for European option pricing:

Call Option Price = S₀N(d₁) - Ke⁻ʳᵗN(d₂)
Put Option Price = Ke⁻ʳᵗN(-d₂) - S₀N(-d₁)

Where:
- S₀ = Current stock price
- K = Strike price
- r = Risk-free rate
- t = Time to maturity
- N() = Cumulative standard normal distribution function
- d₁ = (ln(S₀/K) + (r + σ²/2)t) / (σ√t)
- d₂ = d₁ - σ√t

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Nicolas Pons

## 🙏 Acknowledgments

- Black-Scholes-Merton original paper (1973)
- Financial Python community
- Streamlit documentation and community

## 📚 Additional Resources

- [Black-Scholes Model on Wikipedia](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)
- [Option Greeks Explained](https://www.investopedia.com/trading/getting-to-know-the-greeks/)
- [Streamlit Documentation](https://docs.streamlit.io)
