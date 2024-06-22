import pygame,sys

class Button:
	def __init__(self,text,width,height,pos,elevation, font, display, game):
		#Core attributes 
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]
		
		self.font = font
		self.display = display
		self.game = game
		self.text = text

		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#000000'

		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#000066'
		#text
		self.text_surf = self.font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self, nameType = None, yAnimChange = 0, textOpac = 255, xAnimChange = 0, ready = False):
		# elevation logic 
		self.text_surf = self.font.render(self.text,True,'#FFFFFF')
		self.text_surf.set_alpha(textOpac)
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
		self.original_y_pos -= yAnimChange
		
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.top_rect.x -= xAnimChange
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(self.display,self.bottom_color, self.bottom_rect,border_radius = 6)
		pygame.draw.rect(self.display,self.top_color, self.top_rect,border_radius = 6)
		self.display.blit(self.text_surf, self.text_rect)
		if yAnimChange == 0 and textOpac == 255 and xAnimChange == 0: self.check_click(nameType, (self.game.winW, self.game.winH))
		if nameType == "game" and ready:
			ready = False
			self.game.main()

	def check_click(self, nameType, resolution):
		if self.top_rect.collidepoint((pygame.mouse.get_pos()[0]/(resolution[0]/320), pygame.mouse.get_pos()[1]/(resolution[1]/240))):
			self.top_color = '#000000'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					if nameType == 'menub':
						if self.game.smenu.stage == None:
							if self.game.smenu.open > 10:
								self.game.smenu.change_state("close")
								if self.game.firstTime: self.game.firstTime = False
								self.text = "<"
							else:
								self.game.smenu.change_state("open")
								self.text = ">"
					self.pressed = False
					pass
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = '#000000'