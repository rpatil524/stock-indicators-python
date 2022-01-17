from decimal import Decimal
from typing import Iterable, Optional, TypeVar, overload
from stock_indicators._cslib import CsIndicator
from stock_indicators._cstypes import List as CsList
from stock_indicators._cstypes import Decimal as CsDecimal
from stock_indicators._cstypes import to_pydecimal
from stock_indicators.indicators.common.helpers import RemoveWarmupMixin
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote


@overload
def get_parabolic_sar(quotes: Iterable[Quote],
                      acceleration_step: float = 0.02,
                      max_acceleration_factor: float = 0.2
                      ) -> "ParabolicSARResults[ParabolicSARResult]": ...
# TODO: Uncomment when #82 is fixed.
# @overload
# def get_parabolic_sar(quotes: Iterable[Quote],
#                       acceleration_step: float,
#                       max_acceleration_factor: float,
#                       initial_factor: float
#                       ) -> "ParabolicSARResults[ParabolicSARResult]": ...
def get_parabolic_sar(quotes, acceleration_step = 0.02,
                      max_acceleration_factor = 0.2, initial_factor = None):
    """Get Parabolic SAR calculated.

    Parabolic SAR (stop and reverse) is a price-time based indicator
    used to determine trend direction and reversals.

    Parameters:
        `quotes` : Iterable[Quotes]
            Historical price quotes.

        `acceleration_step` : float, defaults 0.02
            Incremental step size.

        `max_acceleration_factor` : float, defaults 0.2
            Maximum step threshold.

    Returns:
        `ParabolicSARResults[ParabolicSARResult]`
            ParabolicSARResults is list of ParabolicSARResult with providing useful helper methods.

    See more:
         - [Parabolic SAR Reference](https://daveskender.github.io/Stock.Indicators.Python/indicators/ParabolicSar/#content)
         - [Helper Methods](https://daveskender.github.io/Stock.Indicators.Python/utilities/#content)
    """
    initial_factor = initial_factor if initial_factor else acceleration_step
    results = CsIndicator.GetParabolicSar[Quote](CsList(Quote, quotes),
                                                 CsDecimal(acceleration_step),
                                                 CsDecimal(max_acceleration_factor),
                                                 #CsDecimal(initial_factor)
                                                 )

    return ParabolicSARResults(results, ParabolicSARResult)


class ParabolicSARResult(ResultBase):
    """
    A wrapper class for a single unit of Parabolic SAR(stop and reverse) results.
    """

    @property
    def sar(self) -> Optional[Decimal]:
        return to_pydecimal(self._csdata.Sar)

    @sar.setter
    def sar(self, value):
        self._csdata.Sar = CsDecimal(value)

    @property
    def is_reversal(self) -> Optional[bool]:
        return self._csdata.IsReversal

    @is_reversal.setter
    def is_reversal(self, value):
        self._csdata.IsReversal = value


T = TypeVar("T", bound=ParabolicSARResult)
class ParabolicSARResults(RemoveWarmupMixin, IndicatorResults[T]):
    """
    A wrapper class for the list of Parabolic SAR(stop and reverse) results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in C# implementation.
    """