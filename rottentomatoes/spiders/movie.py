# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from lxml import html
from html.parser import HTMLParser
from rottentomatoes.items import RottentomatoesItem
import re
class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['www.rottentomatoes.com/m']
    start_urls = ['http://www.rottentomatoes.com/m/']

    def start_requests(self):
        headers = {'Referer':'https://ads.pubmatic.com/AdServer/js/showad.js',
          'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        base_url = 'https://www.rottentomatoes.com/m/{}/reviews/?page={}&type=user'
        movie_li = ['Avatar','Titanic','star_wars_episode_vii_the_force_awakens','avengers_infinity_war','jurassic_world','marvels_the_avengers','avengers_endgame','furious_7','avengers_age_of_ultron','black_panther_2018','harry_potter_and_the_deathly_hallows_part_2_2011'
            , 'star_wars_the_last_jedi','jurassic_world_fallen_kingdom','frozen_2013','beauty_and_the_beast_2017','incredibles_2','the_fate_of_the_furious','iron_man_3','minions','captain_america_civil_war','aquaman_2018','captain_marvel','transformers_dark_of_the_moon','the_lord_of_the_rings_the_return_of_the_king','skyfall'
            ,'transformers_age_of_extinction','the_dark_knight_rises','toy_story_3','pirates_of_the_caribbean_dead_mans_chest','rogue_one_a_star_wars_story'
            , 'pirates_of_the_caribbean_on_stranger_tides','despicable_me_3','jurassic_park','finding_dory','star_wars_episode_i_the_phantom_menace','1221547-alice_in_wonderland','zootopia','the_hobbit_an_unexpected_journey','the_dark_knight','harry_potter_and_the_sorcerers_stone','despicable_me_2','the_lion_king','the_jungle_book_2016','pirates_of_the_caribbean_3','jumanji_welcome_to_the_jungle','harry_potter_and_the_deathly_hallows_part_1','the_hobbit_the_desolation_of_smaug','the_hobbit_the_battle_of_the_five_armies','finding_nemo','harry_potter_and_the_order_of_the_phoenix ']
        page_li = [5025,69746,878,421,591,1922,317,305,514,390,1081,2522,154,600,219,102,118,887,173,468,299,717,996,46084,916,516,1767,1541,5634,416,715,66,1935,189,2047,1740,267,1073,7249,2017,478,2885,209,15536,129,1202,493,338,27956,11429]
        for i in range(len(movie_li)):
            for j in range(page_li[i]+1)[1:]:
                url = base_url.format(movie_li[i],j)
                yield Request(url,callback=self.parse,dont_filter=True,headers=headers)
    def parse(self, response):
        all = re.findall('<li\sclass="audience-reviews__item">(.*?)</li>', response.text, re.S)

        for i in range(len(all)):
            item = RottentomatoesItem()
            id = re.findall('audience-reviews__name">(.*?)</sp', all[i], re.S)
            star = str(all[i].count('star-display__half') * 0.5 + all[i].count('star-display__filled'))
            time = re.findall('audience-reviews__duration">(.*?)<', all[i], re.S)
            comment = re.findall(
                'audience-reviews__review\sjs-review-text\sclamp\sclamp-8\sjs-clamp">(.*?)<p class="audience-reviews__review--mobile\sjs-review-text\sclamp\sclamp-4\sjs-clamp',
                all[i], re.S)
            movie_name = re.findall('m/m/(.*?)/reviews/\?pa',response.url)
            item['movie_name'] = movie_name[0]
            if len(id)==0:
                item['id'] = ''
            else:
                item['id'] = id[0]
            item['star'] = star
            item['time'] = time[0]
            item['comment'] = comment[0].replace('&#x27;','\'').replace('</p>','')
            yield item


