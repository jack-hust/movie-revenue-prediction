from crawl_update_mojo import *
from crawl_update_tmdb import *
from crawl_update_imdb import *
from crawl_update_critic_metascore import *
from crawl_update_themoviedb import *

if __name__ == '__main__':
    main_mojo()
    main_tmdb()
    main_imdb()
    main_critic_metascore()
    main_themoviedb()