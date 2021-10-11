
from typing import Iterable, Optional, Type
from SkenderStockIndicators._cslib import CsIndicator
from SkenderStockIndicators._cstypes import List as CsList
from SkenderStockIndicators._cstypes import Decimal as CsDecimal
from SkenderStockIndicators._cstypes import to_pydecimal
from SkenderStockIndicators.indicators.common.results import IndicatorResults, ResultBase
from SkenderStockIndicators.indicators.common.quote import Quote

def get_adl(quotes: Iterable[Quote], sma_periods: Optional[int] = None):
    adl_results = CsIndicator.GetAdl[Quote](CsList(Quote, quotes), sma_periods)
    return ADLResults(adl_results, ADLResult)

class ADLResult(ResultBase):
    def __init__(self, adl_result):
        super().__init__(adl_result)

    @property
    def money_flow_multiplier(self):
        return to_pydecimal(self._csdata.MoneyFlowMultiplier)

    @money_flow_multiplier.setter
    def money_flow_multiplier(self, value):
        self._csdata.MoneyFlowMultiplier = CsDecimal(value)

    @property
    def money_flow_volume(self):
        return to_pydecimal(self._csdata.MoneyFlowVolume)

    @money_flow_volume.setter
    def money_flow_volume(self, value):
        self._csdata.MoneyFlowVolume = CsDecimal(value)

    @property
    def adl(self):
        return to_pydecimal(self._csdata.Adl)

    @adl.setter
    def adl(self, value):
        self._csdata.Adl = CsDecimal(value)

    @property
    def adl_sma(self):
        return to_pydecimal(self._csdata.AdlSma)

    @adl_sma.setter
    def adl_sma(self, value):
        self._csdata.AdlSma = CsDecimal(value)

class ADLResults(IndicatorResults[ADLResult]):
    """
    A wrapper class for the list of ADL(Accumulation/Distribution Line) results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in C# implementation.
    """

    def __init__(self, data: Iterable, wrapper_class: Type[ADLResult]):
        super().__init__(data, wrapper_class)

    @IndicatorResults._verify_data
    def to_quotes(self) -> Iterable[Quote]:
        quotes = CsIndicator.ConvertToQuotes(CsList(type(self._csdata[0]), self._csdata))

        return quotes