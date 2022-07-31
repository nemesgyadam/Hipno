"""
The script shows the Theta band power of the EEG signal, for each 6 channels.
Device:
https://mindrove.com/arc/
SDK:
https://github.com/MindRove/SDK_Public
"""

import time
import cv2
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, DetrendOperations
import os
clear = lambda: os.system('cls')
channel_ids = [0,1,2,3,4,5]
window_length = 3
def main():
    BoardShim.enable_dev_board_logger()

    # use synthetic board for demo
    params = BrainFlowInputParams()
    board_id = BoardIds.SYNTHETIC_BOARD.value
    board_descr = BoardShim.get_board_descr(board_id)
    sampling_rate = 500
    board = BoardShim(BoardIds.MINDROVE_WIFI_BOARD, params)
    board.prepare_session()
    board.start_stream()
    time.sleep(window_length)
    nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
   

    while True:
        data = board.get_current_board_data(sampling_rate*window_length) 
        clear()
        for channel_id in channel_ids:
            # optional detrend
            DataFilter.detrend(data[channel_id], DetrendOperations.LINEAR.value)
            psd = DataFilter.get_psd_welch(data[channel_id], nfft, nfft // 2, sampling_rate,
                                        3)

            
            band_power_delta = DataFilter.get_band_power(psd, 0.1, 4.0)
            band_power_theta = DataFilter.get_band_power(psd, 4.0, 8.0)
            band_power_alpha = DataFilter.get_band_power(psd, 7.0, 13.0)
            band_power_beta = DataFilter.get_band_power(psd, 14.0, 30.0)
            band_power_gamma = DataFilter.get_band_power(psd, 30.0, 100.0)
            #print(f'Channel {channel_id} delta: {band_power_delta} theta: {band_power_theta} alpha: {band_power_alpha} beta: {band_power_beta} gamma: {band_power_gamma}')
            print(round(band_power_theta,2))
        k = cv2.waitKey(1) & 0xFF
        time.sleep(0.2)
        # press 'q' to exit
        if k == ord('q'):
            break
        
    board.stop_stream()
    board.release_session()

if __name__ == "__main__":
    main()
