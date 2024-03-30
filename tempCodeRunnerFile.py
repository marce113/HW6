def test_get_highest_box_office_per_year(self):
        test_1 = get_highest_box_office_by_year(2005, 'cache.json')
        self.assertEqual(test_1, ("Harry Potter and the Goblet of Fire", 290469928))
        test_2 = get_highest_box_office_by_year(2019, 'cache.json')
        self.assertEqual(test_2, ('Little Women', 108101214))
        test_3 = get_highest_box_office_by_year(2012, 'cache.json')
        self.assertEqual(test_3, ('The Avengers', 623357910))
        test_4 = get_highest_box_office_by_year(1990, 'cache.json')
        self.assertEqual(test_4, 'No films found')
