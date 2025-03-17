document.addEventListener('DOMContentLoaded', function() {
	const fadeElements = document.querySelectorAll('.fade-in');
	setTimeout(() => {
			fadeElements.forEach(element => {
					element.classList.add('is-visible');
			});
	}, 100);
});