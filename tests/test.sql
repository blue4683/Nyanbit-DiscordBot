DROP TABLE `nyanbit_db`.`userinfo`;
DROP TABLE `nyanbit_db`.`subscriptions`;

CREATE TABLE `nyanbit_db`.`userinfo` (
  `user_id` char(24) NOT NULL,
  `user_name` char(8) DEFAULT NULL,
  `is_admin` tinyint DEFAULT '0',
  `nyanbit` int DEFAULT '0',
  `is_allowed_notification` tinyint DEFAULT '0',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `nyanbit_db`.`subscriptions` (
  `subscriptions_id` int NOT NULL AUTO_INCREMENT,
  `streamer_id` char(24) DEFAULT NULL,
  `subscriber_id` char(24) DEFAULT NULL,
  `subscribed_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`subscriptions_id`),
  UNIQUE KEY `streamer_subscriber` (`streamer_id`,`subscriber_id`),
  KEY `_idx` (`streamer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

INSERT INTO `nyanbit_db`.`userinfo`
(`user_id`,
`user_name`,
`is_admin`,
`nyanbit`,
`is_allowed_notification`)
VALUES
('111111111111111111',
'TEST',
0,
0,
0);
