DROP TABLE IF EXISTS `guilds`;

CREATE TABLE `guilds` (
  `id` varchar(255) NOT NULL,
  `language` varchar(10) DEFAULT NULL,
  `followed_leagues` text,
  `scheduler_channel` text,
  PRIMARY KEY (`id`)
)