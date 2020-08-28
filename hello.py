 def test_video_to_dict(self):
        video = telegram.InlineQueryResultVideo.de_json(self.json_dict, self._bot).to_dict() #=========

        self.assertTrue(self.is_dict(video))
        self.assertDictEqual(self.json_dict, video)
