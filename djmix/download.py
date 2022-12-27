from __future__ import annotations

import os
import logging
import traceback
from typing import TYPE_CHECKING
from yt_dlp import YoutubeDL
from djmix import config, utils

if TYPE_CHECKING:
  from djmix.models import Mix, Track


def download():
  from djmix import mixes
  
  for mix in mixes:
    try:
      mix.download()
    except Exception as e:
      logging.error(f'Failed to download mix: {mix.id}')
      traceback.print_exc()


def download_mix(mix: Mix):
  logging.info(f'=> Start downloading {mix.id}')
  root = config.get_root()
  download_audio(
    url=mix.audio_url,
    path=utils.mkpath(root, 'mixes', f'{mix.id}.mp3')
  )


def download_track(track: Track):
  url = f'https://www.youtube.com/watch?v={track.id}'
  logging.info(f'=> Start downloading track {url}')
  root = config.get_root()
  track_path = utils.mkpath(root, 'tracks', f'{track.id}.mp3')
  download_audio(
    url=url,
    path=track_path,
  )


_throttle_count = 0


def download_audio(url, path, max_throttle=100):
  if os.path.isfile(path):
    logging.info(f'{path} already exists. Skip downloading.')
    return
  
  def throttle_detector(d):
    global _throttle_count
    
    if d['status'] == 'downloading' and d['speed'] is not None:
      speed_kbs = d['speed'] / 1024  # downloading speed in KiB/s
      if speed_kbs < 100:
        _throttle_count += 1
      else:
        _throttle_count = 0
      
      if _throttle_count > max_throttle:
        raise Exception(f'The download speed is throttled more than {max_throttle} times. Aborting.')
  
  params = {
    'format': 'bestaudio',
    'outtmpl': path,
    'postprocessors': [{  # Extract audio using ffmpeg
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
    }],
    'progress_hooks': [throttle_detector],
  }
  with YoutubeDL(params) as ydl:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ydl.download(url)
