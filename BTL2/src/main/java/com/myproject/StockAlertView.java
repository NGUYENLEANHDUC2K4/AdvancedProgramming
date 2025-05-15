package com.myproject;

import java.util.HashMap;
import java.util.Map;

public class StockAlertView implements StockViewer {
    private double alertThresholdHigh;
    private double alertThresholdLow;
    private Map<String, Double> lastAlertedPrices = new HashMap<>();

    public StockAlertView(double highThreshold, double lowThreshold) {
        this.alertThresholdHigh = highThreshold;
        this.alertThresholdLow = lowThreshold;
    }

    @Override
    public void onUpdate(StockPrice stockPrice) {
        String stockCode = stockPrice.getCode();
        double currentPrice = stockPrice.getAvgPrice();
        double lastPrice = lastAlertedPrices.getOrDefault(stockCode, 0.0);
        if (currentPrice >= alertThresholdHigh && currentPrice != lastPrice) {
            alertAbove(stockCode, currentPrice);
            lastAlertedPrices.put(stockCode, currentPrice);
            return;
        } else if (currentPrice <= alertThresholdLow && currentPrice != lastPrice) {
            alertBelow(stockCode, currentPrice);
            lastAlertedPrices.put(stockCode, currentPrice);
            return;
        }
        lastAlertedPrices.put(stockCode, currentPrice);
    }

    private void alertAbove(String stockCode, double price) {
        Logger.logAlert(stockCode, price);
    }

    private void alertBelow(String stockCode, double price) {
        Logger.logAlert(stockCode, price);
    }
}
