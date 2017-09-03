from scene import *
import random


negative_textures = [Texture('card:HeartsA'), Texture('card:Hearts2'), Texture('card:Hearts3'), Texture('card:Hearts4'), Texture('card:Hearts5'), Texture('card:Hearts6'), Texture('card:Hearts7'), Texture('card:Hearts8'), Texture('card:Hearts9'), Texture('card:Hearts10'), Texture('card:HeartsJ'), Texture('card:HeartsQ'), Texture('card:HeartsK')]

positive_textures = [Texture('card:SpadesA'), Texture('card:Spades2'), Texture('card:Spades3'), Texture('card:Spades4'), Texture('card:Spades5'), Texture('card:Spades6'), Texture('card:Spades7'), Texture('card:Spades8'), Texture('card:Spades9'), Texture('card:Spades10'), Texture('card:SpadesJ'), Texture('card:SpadesQ'), Texture('card:SpadesK')]

double_textures = [Texture('card:ClubsA'), Texture('card:Clubs2'), Texture('card:Clubs3'), Texture('card:Clubs4'), Texture('card:Clubs5'), Texture('card:Clubs6'), Texture('card:Clubs7'), Texture('card:Clubs8'), Texture('card:Clubs9'), Texture('card:Clubs10'), Texture('card:ClubsJ'), Texture('card:ClubsQ'), Texture('card:ClubsK')]


class Deck(object):
	def __init__(self, num_list):
		self.cards = []
		for num in num_list:
			if 0<num<=10:
				r = num
				card = Card(r)
			elif 10<num<=20:
				r = (num-10)*-1
				card = Card(r)
			else:
				r = num-20
				card = Card(r,mflag = True)
				
			card.x_scale = 0.5
			card.y_scale = 0.5
			self.cards.append(card)
		self.size = len(self.cards)
		
	def shuffle(self):
		random.shuffle(self.cards)
		
	def add(self, card):
		self.cards.append(card)
		self.size += 1
		
	def remove(self, index):
		card = self.cards.pop(index)
		self.size -= 1
		return card
		
		
class ButtonNode (SpriteNode):
	def __init__(self, title, *args, **kwargs):
		SpriteNode.__init__(self, 'pzl:Button1', *args, **kwargs)
		button_font = ('Avenir Next', 20)
		self.title_label = LabelNode(title, font=button_font, color='black', position=(0, 1), parent=self)
		self.title = title

class Card (SpriteNode):
	def __init__(self, num, mflag = False, **kwargs):
		self.value = num
		self.flag = mflag
		if self.flag:
			self.front = double_textures[num-1]
		else:
			if self.value > 0:
				self.front = positive_textures[num-1]
			else:
				num *= -1
				self.front = negative_textures[num-1]
				
		self.back = Texture('card:BackBlue5')
		SpriteNode.__init__(self, self.back, **kwargs)
		

class Game (Scene):
	def setup(self):
		self.background_color = '#00263f'
		self.buttons = []
		self.buttons.append(ButtonNode('Deal', parent = self, position = (self.size.w*0.9, self.size.h*0.9)))
		self.buttons.append(ButtonNode('Start', parent = self, position = (self.size.w*0.7, self.size.h*0.9)))
		self.buttons.append(ButtonNode('Reset', parent = self, position = (self.size.w*0.5, self.size.h*0.9)))
		self.build_main_deck()
		self.build_side_deck()
				
				
	def build_main_deck(self):
		# Build a standard deck
		num_list = []
		for num in range(10):
			for iter in range(4):
				num_list.append(num+1)
				
		self.main_deck = Deck(num_list)
		self.main_deck.shuffle()
		
		s = self.main_deck.size
		y = 64
		x = self.size.w *0.7
		for i in range(s):
			card = self.main_deck.cards[i]
			card.position = (x,y)
			self.add_child(card)
			if i < 4:
				x -= 8
		
	def build_side_deck(self):
		# Build a ?standard? side deck
		num_list = []
		for num in range(10):
			num_list.append(random.randint(1,30))
		
		self.side_deck = Deck(num_list)
		self.side_deck.shuffle()
		
		num_col = 2
		num_row = 5
		dx = (self.size.w*0.25) / (num_col+1)
		dy = (self.size.h*0.9) / (num_row+1)

		for row in range(num_row):
			for col in range(num_col):
				x = dx + col*dx + self.size.w*0.75
				y = dy + row*dy + 0
				index = row+ col*num_row
				card = self.side_deck.cards[index]
				card.position =(x,y)
				self.add_child(card)
		
	def build_hand(self):
		y = 64
		x = 0
		for i in range(4):
			x += 128
			s = self.side_deck.size
			card = self.side_deck.remove(random.randint(0,s-1))
			make_hand = Action.move_to(x,y,3.0,TIMING_SINODIAL)
			card.run_action(make_hand)
			card.texture = card.front
			
		
	def touch_began(self, touch):
		touch_loc = touch.location
		for btn in self.buttons:
			if touch_loc in btn.frame:
				#sound.play_effect('8ve:8ve-tap-resonant')
				btn.texture = Texture('pzl:Button2')
	
	def touch_ended(self, touch):
		touch_loc = touch.location
		for btn in self.buttons:
			btn.texture = Texture('pzl:Button1')
			if touch_loc in btn.frame:
				self.button_selected(btn.title)
				
	def reset(self):
		for child in self.children:
			child.run_action(Action.sequence(Action.fade_to(0, 0.35), Action.remove()))
		self.setup()
				
	def button_selected(self, title):
		if title.startswith('Start'):
			self.build_hand()
		elif title.startswith('Reset'):
			self.reset()
		elif title.startswith('Deal'):
			pass
			
			
if __name__ == '__main__':
	run(Game(), PORTRAIT, show_fps=True)
