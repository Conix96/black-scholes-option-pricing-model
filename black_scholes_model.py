from typing import Tuple, List, Union
import numpy as np
from numpy import exp, sqrt, log, pi
from scipy.stats import norm
from dataclasses import dataclass


@dataclass
class OptionGreeks:
    """Container for option Greeks."""

    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float


class BlackScholes:
    """
    A class implementing the Black-Scholes option pricing model.

    The model calculates theoretical option prices and Greeks for European-style
    options on non-dividend paying stocks.

    Attributes:
        time_to_maturity (float): Time to option expiration in years
        strike_price (float): Strike price of the option
        current_price (float): Current price of the underlying asset
        volatility (float): Annualized volatility of the underlying asset
        interest_rate (float): Risk-free interest rate (annual)
    """

    def __init__(
        self,
        time_to_maturity: float,
        strike_price: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
    ) -> None:
        """
        Initialize the Black-Scholes model with option parameters.

        Args:
            time_to_maturity: Time to expiration in years
            strike_price: Strike price of the option
            current_price: Current price of the underlying asset
            volatility: Annualized volatility (decimal)
            interest_rate: Risk-free interest rate (decimal)

        Raises:
            ValueError: If any of the input parameters are invalid
        """
        self._validate_inputs(
            time_to_maturity, strike_price, current_price, volatility, interest_rate
        )

        self.time_to_maturity = time_to_maturity
        self.strike_price = strike_price
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

        # Calculate d1 and d2 once since they're used in multiple calculations
        self._d1, self._d2 = self._calculate_d1_d2()

    @staticmethod
    def _validate_inputs(
        time_to_maturity: float,
        strike_price: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
    ) -> None:
        """Validate input parameters."""
        if time_to_maturity <= 0:
            raise ValueError("Time to maturity must be positive")
        if strike_price <= 0:
            raise ValueError("Strike price must be positive")
        if current_price <= 0:
            raise ValueError("Current price must be positive")
        if volatility <= 0:
            raise ValueError("Volatility must be positive")
        if interest_rate < 0:
            raise ValueError("Interest rate cannot be negative")

    def _calculate_d1_d2(self) -> Tuple[float, float]:
        """Calculate d1 and d2 parameters used in Black-Scholes formula."""
        d1 = (
            log(self.current_price / self.strike_price)
            + (self.interest_rate + 0.5 * self.volatility**2) * self.time_to_maturity
        ) / (self.volatility * sqrt(self.time_to_maturity))

        d2 = d1 - self.volatility * sqrt(self.time_to_maturity)
        return d1, d2

    def calculate_prices(self) -> Tuple[float, float]:
        """
        Calculate call and put option prices using the Black-Scholes formula.

        Returns:
            Tuple[float, float]: Call and put option prices
        """
        discount_factor = exp(-self.interest_rate * self.time_to_maturity)

        call_price = self.current_price * norm.cdf(
            self._d1
        ) - self.strike_price * discount_factor * norm.cdf(self._d2)

        put_price = self.strike_price * discount_factor * norm.cdf(
            -self._d2
        ) - self.current_price * norm.cdf(-self._d1)

        return call_price, put_price

    def calculate_greeks(self) -> Tuple[OptionGreeks, OptionGreeks]:
        """
        Calculate option Greeks for both call and put options.

        Returns:
            Tuple[OptionGreeks, OptionGreeks]: Greeks for call and put options
        """
        # Common calculations
        discount_factor = exp(-self.interest_rate * self.time_to_maturity)
        sqrt_t = sqrt(self.time_to_maturity)
        d1_pdf = exp(-self._d1**2 / 2) / sqrt(2 * pi)

        # Call Greeks
        call_delta = norm.cdf(self._d1)
        gamma = d1_pdf / (self.current_price * self.volatility * sqrt_t)

        call_theta = -(
            self.current_price * d1_pdf * self.volatility / (2 * sqrt_t)
        ) - self.interest_rate * self.strike_price * discount_factor * norm.cdf(
            self._d2
        )

        vega = self.current_price * sqrt_t * d1_pdf

        call_rho = (
            self.strike_price
            * self.time_to_maturity
            * discount_factor
            * norm.cdf(self._d2)
        )

        # Put Greeks
        put_delta = call_delta - 1
        put_theta = -(
            self.current_price * d1_pdf * self.volatility / (2 * sqrt_t)
        ) + self.interest_rate * self.strike_price * discount_factor * norm.cdf(
            -self._d2
        )
        put_rho = (
            -self.strike_price
            * self.time_to_maturity
            * discount_factor
            * norm.cdf(-self._d2)
        )

        call_greeks = OptionGreeks(call_delta, gamma, call_theta, vega, call_rho)
        put_greeks = OptionGreeks(put_delta, gamma, put_theta, vega, put_rho)

        return call_greeks, put_greeks

    def calculate_pnl(
        self, spot_range: Union[List[float], np.ndarray], purchase_price: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate the PnL for a range of spot prices based on the purchase price.

        Args:
            spot_range: Array of potential future spot prices
            purchase_price: Price paid for the option

        Returns:
            Tuple[np.ndarray, np.ndarray]: PnL arrays for call and put options

        Raises:
            ValueError: If purchase_price is negative
        """
        if purchase_price < 0:
            raise ValueError("Purchase price cannot be negative")

        spot_range = np.asarray(spot_range)
        if not spot_range.size:
            raise ValueError("Spot range cannot be empty")

        call_pnl = np.maximum(0, spot_range - self.strike_price) - purchase_price
        put_pnl = np.maximum(0, self.strike_price - spot_range) - purchase_price

        return call_pnl, put_pnl
