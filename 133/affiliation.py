def generate_affiliation_link(url):
    id_tag = url.split("/")[5]
    return f'http://www.amazon.com/dp/{id_tag}/?tag=pyb0f-20'
