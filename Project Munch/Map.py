import pygame, os, Loader

DIR_UP = 1
DIR_RIGHT = -1
DIR_DOWN = -1
DIR_LEFT = 1

zoom_factor = 8
class Map():
	def __init__(self, screen):
		main_dir = os.path.split(os.path.abspath(__file__))[0]
		data_dir = os.path.join(main_dir, 'data')
		image, view_rect = Loader.load_image('map.png', -1)
		print ("Map Initialized!")
		
	def scroll_view(screen, mapx, mapy):
		dx = dy = 0
		src_rect = None
		zoom_view_rect = screen.get_clip()
		image_w, image_h = image.get_size()
		if mapy == DIR_UP:
			if view_rect.top > 0:
				screen.scroll(dy=zoom_factor)
				view_rect.move_ip(0, -1)
				src_rect = view_rect.copy()
				src_rect.h = 1
				dst_rect = zoom_view_rect.copy()
				dst_rect.h = zoom_factor
		elif mapy == DIR_DOWN:
			if view_rect.bottom < image_h:
				screen.scroll(dy=-zoom_factor)
				view_rect.move_ip(0, 1)
				src_rect = view_rect.copy()
				src_rect.h = 1
				src_rect.bottom = view_rect.bottom
				dst_rect = zoom_view_rect.copy()
				dst_rect.h = zoom_factor
				dst_rect.bottom = zoom_view_rect.bottom
		elif mapx == DIR_LEFT:
			if view_rect.left > 0:
				screen.scroll(dx=zoom_factor)
				view_rect.move_ip(-1, 0)
				src_rect = view_rect.copy()
				src_rect.w = 1
				dst_rect = zoom_view_rect.copy()
				dst_rect.w = zoom_factor
		elif mapx == DIR_RIGHT:
			if view_rect.right < image_w:
				screen.scroll(dx=-zoom_factor)
				view_rect.move_ip(1, 0)
				src_rect = view_rect.copy()
				src_rect.w = 1
				src_rect.right = view_rect.right
				dst_rect = zoom_view_rect.copy()
				dst_rect.w = zoom_factor
				dst_rect.right = zoom_view_rect.right
		if src_rect is not None:
			scale(image.subsurface(src_rect),
				  dst_rect.size,
				  screen.subsurface(dst_rect))
			pygame.display.update(zoom_view_rect)