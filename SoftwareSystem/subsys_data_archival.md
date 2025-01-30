# COSMIC Data archival

The COSMIC database [entities](https://github.com/COSMIC-SETI/COSMIC-VLA-Database/blob/main/docs/tables.md), and their [relationships](https://github.com/COSMIC-SETI/COSMIC-VLA-Database#cosmic-database), are defined [programmatically](https://github.com/COSMIC-SETI/COSMIC-VLA-Database/blob/main/src/cosmic_database/entities.py).

The database connection is defined at `/home/comsic/conf/cosmic_db_conf.yaml` to be the `cosmic_observations` database in the `mysql` instance running on `cosmic-head`.

<details><summary>Creating the database</summary>
On the `cosmic-storage-1` node, issue the following.

```
mysql -u root -p
SHOW DATABASES;
DROP DATABASE cosmic_observations;
CREATE DATABASE cosmic_observations;

CREATE USER 'cosmic'@'localhost' IDENTIFIED BY '******';
GRANT ALL PRIVILEGES ON cosmic_observations.* TO 'cosmic'@'localhost' WITH GRANT OPTION
CREATE USER 'cosmic'@'%' IDENTIFIED BY '******';
GRANT ALL PRIVILEGES ON cosmic_observations.* TO 'cosmic'@'%' WITH GRANT OPTION
```

Change bind-address value to `0.0.0.0` in `sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf` and `sudo systemctl restart mysql`.

</details>

<details><summary>Viewing the database</summary>
On the `cosmic-head` node, a CloudBeaver instance is running, exposed on port `8079`. In order to expose this port locally on your machine, create an ssh session with the appropriate tunnel parameters: `ssh user@login.aoc.nrao.edu -L 8079:cosmic-head:8079`.

The administrative user is `cbadmin`, with the same password used to execute ipmi commands on the `cosmic-head` node.
The typical user account is `cosmic` with the same password as that user on the `cosmic-head` node.
</details>

<details><summary>Indexing a table's field (for lookup speed-ups)</summary>
```
mysql -u root -p
mysql> ALTER TABLE cosmic_observations.cosmic_observation_hit ADD INDEX tstart_index (tstart);
```
</details>


The entities are populated by services as follows.

Service | Database Entity Populated
-|-
mcast2redis | Dataset
mcast2redis | Scan
observe | ObservationConfiguration
observe | Observation
observe | ObservationSubband
dbarchive (`"vlass-seti"` post-process stage) | ObservationBeam
dbarchive (`"vlass-seti"` post-process stage) | ObservationHit
dbarchive (`"vlass-seti"` post-process stage) | ObservationStamp
