import gymnasium as gym
from sb3_contrib import MaskablePPO
from stable_baselines3 import PPO, DQN

from Player import Player
from ai.yugioh_env import YugiohEnv
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.common.maskable.policies import MaskableMultiInputActorCriticPolicy

# This is a drop-in replacement for EvalCallback
from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback
from sb3_contrib.common.maskable.evaluation import evaluate_policy


def mask_function(env):
    return env.action_mask()


gym.register(id="Yugioh-v0", entry_point=YugiohEnv, max_episode_steps=1000)

env = gym.make("Yugioh-v0")
env = ActionMasker(env, mask_function)

save_name = "yugioh_v1"

training_model = MaskablePPO(
    MaskableMultiInputActorCriticPolicy,
    env,
    verbose=1,
    tensorboard_log="ppo_yugio",
    gamma=0.99)


def train(model):
    model.learn(
        total_timesteps=1_000_000,
        progress_bar=True,
        tb_log_name="AAA",
    )
    model.save(save_name)


def test(env):
    model = MaskablePPO.load(save_name)
    mean_reward, std_reward = evaluate_policy(
        model, env, n_eval_episodes=100, deterministic=True
    )
    with open("results.txt", "a") as f:
        f.write(f"deterministic: mean_reward:{
                mean_reward:.2f} +/- {std_reward:.2f}\n")
    mean_reward, std_reward = evaluate_policy(
        model, env, n_eval_episodes=100, deterministic=False
    )
    with open("results.txt", "a") as f:
        f.write(f"nondeterministic: mean_reward:{
                mean_reward:.2f} +/- {std_reward:.2f}\n")


for i in range(10):
    print(f"Training {i}")
    train(training_model)
    test(env)
