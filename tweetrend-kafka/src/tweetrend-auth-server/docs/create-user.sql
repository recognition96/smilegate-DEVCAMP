CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider_id` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `profile_image_url` varchar(255) DEFAULT NULL,
  `access_token` varchar(255) DEFAULT NULL,
  `access_token_secret` varchar(255) DEFAULT NULL,
  `provider` varchar(255) NOT NULL,
  `role` enum('admin','user') NOT NULL DEFAULT 'user',
  `is_active` tinyint(4) NOT NULL DEFAULT '1',
  `is_locked` tinyint(4) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `accessed_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
