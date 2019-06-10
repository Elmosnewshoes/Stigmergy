# =======================================
# Created by: Bram Durieux
#   as part of the master thesis at the Delft University of Technology
#
# Description: Deploy the database used for the simulator
# =======================================

import sqlite3, sys
from sqlite3 import Error
from cythonic.plugins.db_path import db_path


def create_connection(db_file, qrys):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        cursor = conn.cursor()
        for q in qrys:
            cursor.execute(q)
            print(q)
    except Error as e:
        print(e)
    finally:
        conn.close()

if __name__ == '__main__':
    qry = ["CREATE TABLE \"sim\" ( `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `status` TEXT NOT NULL DEFAULT 'INITIALIZED', `recording` TEXT, `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP, `initializer` TEXT, `steps_recorded` INTEGER , comment text)"]
    qry.append("CREATE TABLE `sim_settings` ( `sim_id` INTEGER NOT NULL UNIQUE, `n_agents` integer, `dt` numeric, `steps` integer, `deploy_style` text, `deploy_timing` text, `deploy_timing_args` text, `evap_rate` numeric, discrete integer(1) default 1, FOREIGN KEY(`sim_id`) REFERENCES `sim`(`ID`) ON DELETE CASCADE, PRIMARY KEY(`sim_id`) )")
    qry.append("CREATE TABLE \"step\" ( `SIM_ID` INTEGER NOT NULL, `STEP_NR` INTEGER NOT NULL, `ANT_ID` INTEGER NOT NULL, `X` NUMERIC NOT NULL, `Y` NUMERIC NOT NULL, `THETA` NUMERIC NOT NULL, `Q` NUMERIC NOT NULL, FOREIGN KEY(`SIM_ID`) REFERENCES `sim`(`ID`) )")
    qry.append("CREATE TABLE \"ant_settings\" ( `sim_id` INTEGER NOT NULL UNIQUE, `l` NUMERIC, `sens_offset` NUMERIC, `gain` NUMERIC, `noise_gain` NUMERIC, `sens_fun` TEXT, `deposit_fun` TEXT, rotate_fun TEXT, noise_gain2 NUMERIC, steer_regularization NUMERIC DEFAULT 0, d numeric, override_time numeric, override_max numeric, override text, FOREIGN KEY(`sim_id`) REFERENCES `sim`(`ID`) ON DELETE CASCADE, PRIMARY KEY(`sim_id`) )")
    qry.append("CREATE TABLE `deposit_settings` ( `sim_id` INTEGER NOT NULL UNIQUE, `q` numeric, `return_factor` numeric, `beta` numeric, FOREIGN KEY(`sim_id`) REFERENCES `sim`(`ID`) ON DELETE CASCADE, PRIMARY KEY(`sim_id`) )")
    qry.append("CREATE TABLE `domain_settings` ( `sim_id` INTEGER NOT NULL UNIQUE, `size` TEXT, `pitch` NUMERIC, `nest_loc` TEXT, `nest_rad` integer, `food_loc` TEXT, `food_rad` integer, target_pheromone NUMERIC, FOREIGN KEY(`sim_id`) REFERENCES `sim`(`ID`) ON DELETE CASCADE, PRIMARY KEY(`sim_id`) )")
    qry.append("CREATE TABLE `gauss_settings` ( `sim_id` INTEGER NOT NULL UNIQUE, `significancy` NUMERIC, `covariance` NUMERIC, FOREIGN KEY(`sim_id`) REFERENCES `sim`(`ID`) ON DELETE CASCADE, PRIMARY KEY(`sim_id`) )")
    qry.append("CREATE TABLE `queen_settings` ( `sim_id` INTEGER NOT NULL UNIQUE, `default_speed` NUMERIC, `noise_type` TEXT, `noise_parameter` NUMERIC, FOREIGN KEY(`sim_id`) REFERENCES `sim`(`ID`) ON DELETE CASCADE, PRIMARY KEY(`sim_id`) )")
    qry.append("CREATE TABLE \"results\" ( `sim_id` INTEGER NOT NULL UNIQUE, `entropy_vec` text, `start_entropy` numeric, `end_entropy` numeric, `foodcount` integer, `nestcount` integer, `scorecard` TEXT, `step_vec` TEXT, pheromone_max NUMERIC, FOREIGN KEY(`sim_id`) REFERENCES `sim`(`ID`) ON DELETE CASCADE, PRIMARY KEY(`sim_id`) )")
    qry.append("CREATE TABLE `sens_settings` ( `sim_id` INTEGER NOT NULL UNIQUE, `breakpoint` numeric, `exp_lambda` numeric, FOREIGN KEY(`sim_id`) REFERENCES `sim`(`ID`) ON DELETE CASCADE, PRIMARY KEY(`sim_id`) )")
    path = db_path()+"stigmergy.db"
    print(path)
    create_connection(path, qry)
