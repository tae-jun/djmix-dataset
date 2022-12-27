from __future__ import annotations

import os
import abc
from typing import Optional, Tuple, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
  from numpy.typing import NDArray
  from pydub import AudioSegment
  from madmom.audio.signal import Signal


class Audio(BaseModel, abc.ABC):
  
  def beats(self, **kwargs):
    from djmix import features
    return features.corrected_beats(self, **kwargs)
  
  def halfbeat_chroma(self, **kwargs):
    from djmix import features
    return features.halfbeat_chroma(self, **kwargs)
  
  def halfbeat_mfcc(self, **kwargs):
    from djmix import features
    return features.halfbeat_mfcc(self, **kwargs)
  
  def melspectrogram(self, **kwargs):
    from djmix import features
    return features.melspectrogram(self, **kwargs)
  
  def cqt(self, **kwargs):
    from djmix import features
    return features.cqt(self, **kwargs)
  
  def numpy(self, sr=None, mono=True, normalize=False) -> Tuple[NDArray, int]:
    from djmix.audio import load_audio
    return load_audio(self.path, sr=sr, mono=mono, normalize=normalize, format='numpy')
  
  def pydub(self, sr=None, mono=True, normalize=False) -> Tuple[AudioSegment, int]:
    from djmix.audio import load_audio
    return load_audio(self.path, sr=sr, mono=mono, normalize=normalize, format='pydub')
  
  def madmom(self, sr=None, mono=True, normalize=False) -> Tuple[Signal, int]:
    from djmix.audio import load_audio
    return load_audio(self.path, sr=sr, mono=mono, normalize=normalize, format='madmom')
  
  def exists(self):
    if self.path is None:
      return False
    
    if os.path.isfile(self.path):
      return True
    
    return False
  
  @property
  @abc.abstractmethod
  def path(self) -> str:
    pass
  
  @abc.abstractmethod
  def download(self):
    pass
