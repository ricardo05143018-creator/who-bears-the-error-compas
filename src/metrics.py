"""
Phase 1C: Centralized metric definitions for threshold evaluation.
Date: August 2026
"""

import numpy as np


# return NaN instead of 0 to handle undefined endpoints properly.
def safe_div(n, d):
    return float(n) / d if d > 0 else float('nan')


def confusion_counts(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    tp = np.sum((y_true == 1) & (y_pred == 1))
    return int(tn), int(fp), int(fn), int(tp)


def fpr(fp, tn): return safe_div(fp, fp + tn)


def fnr(fn, tp): return safe_div(fn, fn + tp)


def ppv(tp, fp): return safe_div(tp, tp + fp)


def npv(tn, fn): return safe_div(tn, tn + fn)


def tpr(fnr_val): return 1.0 - fnr_val if not np.isnan(fnr_val) else float('nan')


def tnr(fpr_val): return 1.0 - fpr_val if not np.isnan(fpr_val) else float('nan')


def accuracy(tp, tn, n): return safe_div(tp + tn, n)


def balanced_accuracy(tpr_val, tnr_val): return (tpr_val + tnr_val) / 2.0 if not (
            np.isnan(tpr_val) or np.isnan(tnr_val)) else float('nan')


def overall_error(fp, fn, n): return safe_div(fp + fn, n)


def selection_rate(tp, fp, n): return safe_div(tp + fp, n)


def classification_metrics(y_true, y_pred):
    tn, fp, fn, tp = confusion_counts(y_true, y_pred)
    n = tn + fp + fn + tp

    m_fpr = fpr(fp, tn)
    m_fnr = fnr(fn, tp)
    m_tpr = tpr(m_fnr)
    m_tnr = tnr(m_fpr)

    return {
        'n': n, 'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn,
        'fpr': m_fpr,
        'fnr': m_fnr,
        'ppv': ppv(tp, fp),
        'npv': npv(tn, fn),
        'tpr_recall': m_tpr,
        'tnr_spec': m_tnr,
        'accuracy': accuracy(tp, tn, n),
        'balanced_accuracy': balanced_accuracy(m_tpr, m_tnr),
        'overall_error': overall_error(fp, fn, n),
        'selection_rate': selection_rate(tp, fp, n)
    }