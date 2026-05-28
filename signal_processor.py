# signal_processor.py
# Modul 4: Demultiplexing signálu a Epoch Folding algoritmus

class SignalProcessor:
    @staticmethod
    def epoch_folding(photon_timestamps, period, num_bins=30):
        bins = [0] * num_bins
        for t in photon_timestamps:
            phase = (t % period) / period
            bin_idx = int(phase * num_bins)
            if 0 <= bin_idx < num_bins:
                bins[bin_idx] += 1
        return bins