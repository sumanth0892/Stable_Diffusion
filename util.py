"""
This script contains the utils, i.e. helper files for the entire module
"""
import os
import torch
import numpy as np

def get_time_embedding(timestep, dtype):
	"""
	Takes a timestep as an input and gives the embedding
	Look at this in the notebook
	"""
	freqs = torch.pow(10000, -torch.arange(start = 0, end = 160, dtype = dtype) / 160)
	x = torch.tensor([timestep], dtype = dtype)[:, None] * freqs[None]
	return torch.cat([torch.cos(x), torch.sin(x)], dim = 1)

def get_alphas_cumprod(beta_start = -0.00085, beta_end = 0.0120, n_training_steps = 1000):
	"""
	Understand this through the notebook
	"""
	betas = np.linspace(beta_start ** 0.5, beta_end ** 0.5, n_training_steps, dtype = np.float32) ** 2
	alphas = 1.0 - betas
	alphas_cumprod = np.cumprod(alphas, axis = 0)
	return alphas_cumprod

def get_file_path(filename, url = None):
	module_location = os.path.dirname(os.path.abspath(__file__))
	parent_location = os.path.dirname(module_location)
	file_location = os.path.join(parent_location, "data", filename)
	return file_location

def move_channel(image, to):
	if to == 'first':
		return image.permute(0, 3, 1, 2) # (N, H, W, C) -> (N, C, H, W)
	elif to == 'last':
		return image.permute(0, 2, 3, 1) # (N, C, H, W) -> (N, H, W, C)
	else:
		print("to value must be either first or last")

def rescale(x, old_range, new_range, clamp = False):
	old_min, old_max = old_range
	new_min, new_max = new_range
	x -= old_min
	x *= (new_max - new_min) / (old_max - old_min)
	x += new_min
	if clamp:
		x  = x.clamp(new_min, new_max)
	return x