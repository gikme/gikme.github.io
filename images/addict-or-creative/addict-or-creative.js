(function () {

	var Game = function (staticPathPrefix) {
		var host = document.querySelector('#addict-or-creative');
		if (host === null) {
			throw new Error('Host not found');
		}
		this.host = host;
		this.staticPathPrefix = staticPathPrefix;
		this.init();
	};

	Game.prototype.states = {
		PENDING: 0,
		PLAYING: 1,
		FINISHED: 2
	};
	Game.prototype.steps = [];
	Game.prototype.currentState = null;
	Game.prototype.scores = 0;
	Game.prototype.step = 0;
	Game.prototype.host = null;
	Game.prototype.image = null;
	Game.prototype.imageBuffer = new Image;
	Game.prototype.init = function () {
		var self = this;
		var css = document.createElement('link');
		css.rel = 'stylesheet';
		css.href = self.staticPathPrefix + 'aoc.min.css';
		document.head.appendChild(css);
		var yaShare = document.createElement('script');
		yaShare.src = 'http://yastatic.net/share/share.js';
		document.head.appendChild(yaShare);
		self.currentState = this.states.PENDING;
		self.host.innerHTML = StartScreen;
		self.host.addEventListener('click', function (event) {
			var actionId = event.target.getAttribute('data-action');
			switch (actionId) {
				case 'js-aoc--start':
					self.startGame();
					break;
				case 'js-aoc--addict':
					self.turn(true);
					break;
				case 'js-aoc--creative':
					self.turn(false);
					break;
			}
		});
	};
	Game.prototype.startGame = function () {
		var self = this;
		self.steps = shuffle(steps).slice(10);
		self.step = 0;
		self.scores = 0;
		self.currentState = self.states.PLAYING;
		self.host.innerHTML = BattleField;
		self.image = self.host.querySelector('#js-aoc--image');
		self.counter = self.host.querySelector('#aoc--js-counter');
		self.updateImage();
		self.updateCounter();
	};
	Game.prototype.turn = function (isAddict) {
		var self = this;
		
		if (self.steps[self.step].isAddict === isAddict) {
			self.scores += 10;
		}

		self.step += 1;
		
		if (self.step > 9) {
			self.endGame();
		} else {
			self.updateImage();
			self.updateCounter();
		}
	}
	Game.prototype.endGame = function () {
		var self = this;
		self.host.innerHTML = EndScreen;
		var scores = self.host.querySelector('.js-aoc--scores-amount');
		scores.innerHTML = self.scores;
		new Ya.share({
			element: 'aoc--js-share',
			image: self.staticPathPrefix + 'logo.png',
			title: 'Игра Норкоман или творец',
			description: 'Я набрал ' + self.scores + ' очков в игре Норкоман или творец',
			serviceSpecific: {
				twitter: {
					title: 'Я набрал ' + self.scores + ' очков в игре Норкоман или творец'
				}
			},
			elementStyle: {
				type: 'none',
				quickServices: ['', 'vkontakte', 'twitter', 'facebook', 'gplus']
			}
		});
	}
	Game.prototype.updateImage = function () {
		var self = this;
		self.image.src = self.staticPathPrefix + self.steps[self.step].src;
	}
	Game.prototype.updateCounter = function (){
		var self = this;
		self.counter.innerHTML = self.step + 1 + '/10';
	}

	var StartScreen = ''
		+ '<div class="aoc--screen aoc--start">'
			+ '<button class="aoc--button aoc-button_start" data-action="js-aoc--start">'
				+ 'Играть'
			+ '</button>'
		+ '</div>';
	var BattleField = ''
		+ '<div class="aoc--screen aoc--battle-field">'
			+ '<h1 class="aoc--battle-field__header">Норкоман или творец?</h1>'
			+ '<div class="aoc--battle-field__counter" id="aoc--js-counter"></div>'
			+ '<img class="aoc--battle-field__image" id="js-aoc--image">'
			+ '<div class="aoc--battle-field__actions">'
				+ '<button class="aoc--button aoc--button_addict" data-action="js-aoc--addict">'
					+ 'Норкоман'
				+ '</button>'
				+ '<button class="aoc--button aoc--button_creative" data-action="js-aoc--creative">'
					+ 'Творец'
				+ '</button>'
			+ '</div>'
		+ '</div>';
	var EndScreen = ''
		+ '<div class="aoc--screen aoc--end">'
			+ '<h1 class="aoc--hightscores">'
				+ 'Вы набрали <span class="js-aoc--scores-amount"></span> очков'
			+ '</h1>'
			+ '<button class="aoc--button aoc-button_start" data-action="js-aoc--start">'
				+ 'Еще раз!'
			+ '</button>'
			+ '<div id="aoc--js-share"></div>'
		+ '</div>';

	var steps = [
		{src: 'img/1.jpg', isAddict: true},
		{src: 'img/2.jpg', isAddict: true},
		{src: 'img/3.jpg', isAddict: true},
		{src: 'img/4.jpg', isAddict: true},
		{src: 'img/5.jpg', isAddict: true},
		{src: 'img/6.jpg', isAddict: true},
		{src: 'img/7.jpg', isAddict: true},
		{src: 'img/8.jpg', isAddict: true},
		{src: 'img/9.jpg', isAddict: true},
		{src: 'img/10.jpg', isAddict: true},
		{src: 'img/11.jpg', isAddict: false},
		{src: 'img/12.jpg', isAddict: false},
		{src: 'img/13.jpg', isAddict: false},
		{src: 'img/14.jpg', isAddict: false},
		{src: 'img/15.jpg', isAddict: false},
		{src: 'img/16.jpg', isAddict: false},
		{src: 'img/17.jpg', isAddict: false},
		{src: 'img/18.jpg', isAddict: false},
		{src: 'img/19.jpg', isAddict: false},
		{src: 'img/20.jpg', isAddict: false}
	];

	function shuffle(array) {
		var currentIndex = array.length;
		var temporaryValue = 0;
		var randomIndex = 0;

		// While there remain elements to shuffle...
		while (0 !== currentIndex) {

			// Pick a remaining element...
			randomIndex = Math.floor(Math.random() * currentIndex);
			currentIndex -= 1;

			// And swap it with the current element.
			temporaryValue = array[currentIndex];
			array[currentIndex] = array[randomIndex];
			array[randomIndex] = temporaryValue;
		}

		return array;
	}

	new Game('/images/addict-or-creative/');

})();