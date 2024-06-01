document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.slider-wrapper').forEach((sliderWrapper) => {
    const slidesContainer = sliderWrapper.querySelector('.slides-container');
    const slide = sliderWrapper.querySelector('.slide');
    const prevButton = sliderWrapper.querySelector('.slide-arrow[data-slide^="prev"]');
    const nextButton = sliderWrapper.querySelector('.slide-arrow[data-slide^="next"]');

    nextButton.addEventListener('click', () => {
      const slideWidth = slide.clientWidth;
      slidesContainer.scrollLeft += slideWidth;
    });

    prevButton.addEventListener('click', () => {
      const slideWidth = slide.clientWidth;
      slidesContainer.scrollLeft -= slideWidth;
    });
  });
});
