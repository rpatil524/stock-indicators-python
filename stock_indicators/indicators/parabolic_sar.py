from typing import Iterable, Optional, Type, TypeVar, overload
from stock_indicators._cslib import CsIndicator
from stock_indicators._cstypes import List as CsList
from stock_indicators._cstypes import Decimal as CsDecimal
from stock_indicators._cstypes import to_pydecimal
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
def get_parabolic_sar(quotes,
                      acceleration_step = 0.02,
                      max_acceleration_factor = 0.2,
                      initial_factor = None):
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
    def sar(self):
        return to_pydecimal(self._csdata.Sar)

    @sar.setter
    def sar(self, value):
        self._csdata.Sar = CsDecimal(value)
    
    @property
    def is_reversal(self):
        return self._csdata.IsReversal
    
    @is_reversal.setter
    def is_reversal(self, value):
        self._csdata.IsReversal = value

T = TypeVar("T", bound=ParabolicSARResult)
class ParabolicSARResults(IndicatorResults[T]):
    """
    A wrapper class for the list of Parabolic SAR(stop and reverse) results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in C# implementation.
    """

    def __init__(self, data: Iterable, wrapper_class: Type[T]):
        super().__init__(data, wrapper_class)

    @IndicatorResults._verify_data
    def remove_warmup_periods(self, remove_periods: Optional[int] = None):
        if remove_periods is not None:
            return super().remove_warmup_periods(remove_periods)

        removed_results = CsIndicator.RemoveWarmupPeriods(CsList(type(self._csdata[0]), self._csdata))

        return self.__class__(removed_results, self._wrapper_class)
        