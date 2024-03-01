import json
from abc import ABC
from copy import copy

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from config_edit import Components
from connector import RewardProcessor, run_command_and_read_last_line


class AMLEnv(gym.Env, ABC):
    def __init__(self, env_config=None):
        """
        :param env_config: environment configuration
        """
        config = {
            'lives': 1,
            'terminal': True
        }
        if env_config is not None:
            for key in env_config:
                if key in config:
                    config[key] = env_config[key]
        self.lives = config['lives']  # max wrong moves
        self.terminal = config['terminal']
        self.max_episode_steps = self.lives
        self.config_conv = Components()
        self._steps_counter = 0

        self.best_result = {"F1": 0.91, "config": {}}  # save results only about F1 = 0.91
        # prepare obs state and action space
        self.action_space = spaces.MultiDiscrete([3, 3, 3, 50, 2, 4, 3, 7, 4, 7, 4, 5])
        self.observation_state = {
            i: np.zeros((12,), dtype=np.int64)
            for i in range(0, self.max_episode_steps + 1)
        }
        if not self.terminal:
            self.lib_instance = RewardProcessor()
        self.observation_state = {
            i: np.zeros((12,), dtype=np.int64)
            for i in range(0, self.max_episode_steps + 1)
        }

        self.observation_space = spaces.Dict({
            i: self.action_space
            for i in range(0, self.max_episode_steps + 1)
        })

    def reset(self, seed=None, options=None):
        self.observation_state = {
            i: np.zeros((12,), dtype=np.int64)
            for i in range(0, self.max_episode_steps + 1)
        }
        self._steps_counter = 0
        return copy(self.observation_state), {}

    def step(self, action):
        terminate = False
        self._steps_counter += 1
        if action in self.action_space:
            self.observation_state[self._steps_counter - 1] = action

            done, reward = self._calculate_reward(action)
            return copy(self.observation_state), reward, True, terminate, {}
        else:
            return copy(self.observation_state), -100, False, True, {}

    def _calculate_reward(self, action):
        converted_action_list = self.config_conv.convert_action_to_conf(action)
        if self.terminal:
            reward, all_lines = run_command_and_read_last_line(converted_action_list)
        else:
            reward = self.lib_instance.execute(converted_action_list)
        score = {"F1": reward, "config": np.array_str(action)}
        if score["F1"] > self.best_result["F1"]:
            self.best_result = score
            self.save_best_result()
        if reward >= 0.91:
            calc_reward = reward * 250
            return True, calc_reward
        elif reward >= 0.80:
            calc_reward = reward * 200
            return True, calc_reward
        elif reward >= 0.60:
            calc_reward = reward * 150
            return True, calc_reward
        else:
            calc_reward = reward * 100
            return True, calc_reward,

    def save_best_result(self):
        # Save the best result to a file or database
        with open("best_results.txt", "a") as file:
            json.dump(self.best_result, file)
            file.write("\n")
