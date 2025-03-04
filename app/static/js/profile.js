document.addEventListener('DOMContentLoaded', function() {
	const fadeElements = document.querySelectorAll('.fade-in');
	
	const observer = new IntersectionObserver((entries) => {
			entries.forEach(entry => {
					if (entry.isIntersecting) {
							entry.target.classList.add('is-visible');
					}
			});
	}, {
			threshold: 0.1
	});
	
	fadeElements.forEach(element => {
			observer.observe(element);
	});
});