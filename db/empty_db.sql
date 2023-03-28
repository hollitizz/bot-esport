DROP TABLE IF EXISTS `guilds`;

CREATE TABLE `guilds` (
  `id` varchar(255) NOT NULL,
  `language` varchar(10) DEFAULT "en-US",
  `followed_leagues` text DEFAULT NULL,
  `scheduler_channel` text DEFAULT NULL,
  `last_message` text DEFAULT NULL,
  PRIMARY KEY (`id`)
)