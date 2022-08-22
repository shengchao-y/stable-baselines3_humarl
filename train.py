import gym
import os
env = gym.make("Humanoid-v3")

from stable_baselines3 import SAC
from stable_baselines3.common.callbacks import CheckpointCallback

dir_log = "log/humanoid/local_masac_1/"
net_arch = [128, 128]

if os.path.isdir(os.path.join(dir_log, "checkpoint/")) and os.listdir(os.path.join(dir_log, "checkpoint/")):
    files = os.listdir(os.path.join(dir_log, "checkpoint/"))
    last_checkstep = max([int(file.split("_")[-2]) for file in files if file.split("_")[-3]=='model'])
    path_checkpoint = os.path.join(dir_log, "checkpoint/", f"model_{last_checkstep}_steps")
    path_buffer = os.path.join(dir_log, "checkpoint/", f"buffer_{last_checkstep}_steps")
    model = SAC.load(path_checkpoint)
    model.load_replay_buffer(path_buffer)
else:
    model = SAC("HumarlPolicy", env, verbose=1, learning_starts=10000,
        seed=61, policy_kwargs={"net_arch": net_arch}, tensorboard_log=os.path.join(dir_log, "tb/"))

checkpoint_callback = CheckpointCallback(save_freq=60000, save_path=os.path.join(dir_log, "checkpoint/"), name_prefix='model')

model.learn(total_timesteps=10000000, callback=checkpoint_callback)