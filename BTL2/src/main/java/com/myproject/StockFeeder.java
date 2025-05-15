package com.myproject;

import java.util.*;

public class StockFeeder {
    private List<Stock> stockList = new ArrayList<>();
    private Map<String, List<StockViewer>> viewers = new HashMap<>();
    private static StockFeeder instance = null;

    private StockFeeder() {
    }

    public static StockFeeder getInstance() {
        if (instance == null) {
            instance = new StockFeeder();
        }
        return instance;
    }

    public void addStock(Stock stock) {
        if (!stockList.contains(stock)) {
            stockList.add(stock);
            viewers.computeIfAbsent(stock.getCode(), k -> new ArrayList<StockViewer>());
        }
    };

    public void registerViewer(String code, StockViewer stockViewer) {
        boolean stockExists = false;
        for (Stock stock : stockList) {
            if (stock.getCode() == code) {
                stockExists = true;
                break;
            }
        }
        if (!stockExists) {
            Logger.errorRegister(code);
            return;
        }
        List<StockViewer> viewerList = viewers.get(code);
        if (viewerList != null && viewerList.contains(stockViewer)) {
            Logger.errorRegister(code);
            return;
        }
        viewers.computeIfAbsent(code, k -> new ArrayList<StockViewer>()).add(stockViewer);
    }

    public void unregisterViewer(String code, StockViewer stockViewer) {
        boolean stockExists = false;
        for (Stock stock : stockList) {
            if (stock.getCode() == code) {
                stockExists = true;
                break;
            }
        }
        if (!stockExists) {
            Logger.errorUnregister(code);
            return;
        }
        List<StockViewer> viewerList = viewers.get(code);
        if (viewerList.isEmpty() || !viewerList.contains(stockViewer)) {
            Logger.errorUnregister(code);
            return;
        }
        viewers.get(code).remove(stockViewer);
    }

    public void notify(StockPrice stockPrice) {
        if (stockPrice == null) {
            return;
        }
        String code = stockPrice.getCode();
        List<StockViewer> viewerList = viewers.get(code);
        if (viewerList != null) {
            for (StockViewer viewer : viewerList) {
                viewer.onUpdate(stockPrice);
            }
        }
    }
}
