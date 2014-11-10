import math

class VennDiagram:

	def __init__(self, area_a, area_b, intersection, error_scale=0.0001):
		self.area_a = area_a
		self.area_b = area_b
		self.intersection = min([intersection, area_a, area_b])
		self.error = abs(error_scale * intersection)
		self.r1 = math.sqrt(float(area_a) / math.pi)
		self.r2 = math.sqrt(float(area_b) / math.pi)
		
		if intersection > self.error:
			self.distance = VennDiagram._distance(r1=self.r1, 
												  r2=self.r2, 
												  a=self.intersection, 
												  min_d=abs(self.r1-self.r2), 
												  max_d=self.r1+self.r2, 
												  eta=self.error)
		else:
			self.distance = self.r1 + self.r2 # no overlap
		
		
	def __repr__(self):
		return "VennDiagram(%f, %f, %f, %f)" % (self.area_a, self.area_b, self.intersection, self.error)
		
		
	def __str__(self):
		return "radius_a: %f\nradius_b: %f\ndistance: %f" % (self.r1, self.r2, self.distance)
		
		
	def _repr_svg_(self):
		margin = 20
		scale = 100 / max([self.r1, self.r2])
		vs = { 'height':   margin + max([self.r1, self.r2])*2*scale + margin,
			   'offset_y': margin + max([self.r1, self.r2])*scale,
			   'width':    margin + self.r1*scale + self.distance*scale + self.r2*scale + margin,
			   'offset_a': margin + self.r1*scale,
			   'offset_b': margin + self.r1*scale + self.distance*scale,
			   'radius_a': self.r1*scale,
			   'radius_b': self.r2*scale }

		return """<svg height="%(height)f" version="1.0" width="%(width)f" xmlns="http://www.w3.org/2000/svg">
					<circle r="%(radius_a)f" cx="%(offset_a)f" cy="%(offset_y)f" fill="#ff0000" opacity="0.4" />
					<circle r="%(radius_b)f" cx="%(offset_b)f" cy="%(offset_y)f" fill="#0000ff" opacity="0.4" />
				  </svg>""" % vs
	
	
	@staticmethod
	def intersection_area(r1, r2, d):
		"""Computes the intersection area of 2 overlapping circles.
			
			This was lifted from `Wolfram <http://mathworld.wolfram.com/Circle-CircleIntersection.html>`__.

			$$A = r_a^2 \cos^{-1}{\dfrac{d^2 + r_a^2 - r_b^2}{2 d \cdot r_a}} 
				+ r_b^2 \cos^{-1}{\dfrac{d^2 + r_b^2 - r_a^2}{2 d \cdot r_b}}
				- \dfrac{1}{2} \sqrt{(-d+r_a+r_b)(d+r_a-r_b)(d-r_a+r_b)(d+r_a+r_b)}$$
		"""
    
		return (r1**2 * math.acos((d**2 + r1**2 - r2**2) / (2*d*r1)) 
			  + r2**2 * math.acos((d**2 + r2**2 - r1**2) / (2*d*r2)) 
			  - 0.5 * math.sqrt((-d+r1+r2) * (d+r1-r2) * (d-r1+r2) * (d+r1+r2)))
				
				
	@staticmethod
	def _distance(r1, r2, a, min_d, max_d, eta):
		"""Computes the distance two overlapping circles should be apart to have the specified intersection area."""
		
		d = (max_d+min_d) / 2
		guess = VennDiagram.intersection_area(r1, r2, d)
		
		if abs(guess - a) < eta:
			return d
		
		# too much overlap, need more separation
		if guess > a:
			return VennDiagram._distance(r1, r2, a, d, max_d, eta)
			
		# else case, too little overlap, need less separation
		return VennDiagram._distance(r1, r2, a, min_d, d, eta)
	