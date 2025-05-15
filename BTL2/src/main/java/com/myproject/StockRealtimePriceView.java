package com.myproject;

import java.util.HashMap;
import java.util.Map;

public class StockRealtimePriceView implements StockViewer {
    private final Map<String, Double> lastPrices = new HashMap<>();

    @Override
    public void onUpdate(StockPrice stockPrice) {
        String code = stockPrice.getCode();
        double avgPrice = stockPrice.getAvgPrice();
        if (!lastPrices.containsKey(code)) {
            lastPrices.put(code, avgPrice);
            Logger.logRealtime(code, avgPrice);
        } else if (avgPrice != lastPrices.get(code)) {
            lastPrices.put(code, avgPrice);
            Logger.logAlert(code, avgPrice);
        }
    }
}
