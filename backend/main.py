import hydra
from omegaconf import DictConfig

from mortality_fact_updater import MortalityFactUpdater


CONFIG_PATH = 'config'
CONFIG_NAME = 'config'


@hydra.main(config_path=CONFIG_PATH, config_name=CONFIG_NAME)
def main(cfg: DictConfig) -> None:
    mortality_fact_updater = MortalityFactUpdater(cfg=cfg)
    mortality_fact_updater.update_db()


if __name__=='__main__':
    main()
