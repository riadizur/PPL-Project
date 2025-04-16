let currentHotelCount = 0; // Track the current number of Hotels loaded
const HotelsPerLoad = 5; // Number of Hotels to load each time
let allHotelListings = []; // Store all Hotel listings for filtering
let currentFilterQualification = ''; // Store the current qualification filter
let currentFilterHotelType = ''; // Store the current Hotel type filter
// Show the modal with hotel details
const showHotelModal = (hotel) => {
    const modal = document.getElementById('hotelModal');
    const modalImage = document.getElementById('modalImage');
    const modalName = document.getElementById('modalName');
    const modalDescription = document.getElementById('modalDescription');
    const modalFacilities = document.getElementById('modalFacilities');

    // Set modal content
    modalImage.style.backgroundImage = `url("${hotel.image}")`;
    modalName.textContent = hotel.name;
    modalDescription.textContent = hotel.description; // Assuming hotel has a description field
    modalFacilities.textContent = hotel.facility; // Clear existing facilities
    // hotel.facilities.forEach(facility => { // Assuming facilities is an array
    //     const listItem = document.createElement('li');
    //     listItem.textContent = facility;
        // modalFacilities.appendChild(listItem);
    // });

    // Show the modal
    modal.style.display = 'flex';
};

// Close the modal when the close button is clicked
document.getElementById('modalClose').onclick = () => {
    const modal = document.getElementById('hotelModal');
    modal.style.display = 'none'; 
};

// Function to fetch Hotel listings from the server with offset and limit
const fetchHotelListings = async (offset, limit) => {
    const response = await fetch(`/api/v1/hotels?offset=${offset}&limit=${limit}`);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};

// Function to load Hotel listings
const loadHotelListings = async (searchTerm = '') => {
    try {
        const HotelListings = await fetchHotelListings(currentHotelCount, HotelsPerLoad); // Fetch Hotels with offset and limit

        // // Pause for debugging here
        // debugger; // This line will pause execution when running in a browser with developer tools open

        // Store all Hotel listings for future searches
        allHotelListings = allHotelListings.concat(HotelListings);

        const HotelContainer = document.querySelector('.grid');
        HotelContainer.innerHTML = ''; // Clear the container for new listings

        // Filter Hotels based on search term, qualification, and Hotel type
        const filteredHotels = allHotelListings.filter(Hotel => {
            const matchesSearchTerm = Hotel.name.toLowerCase().includes(searchTerm.toLowerCase());
            const matchesQualification = currentFilterQualification ? Hotel.qualification === currentFilterQualification : true;
            const matchesHotelType = currentFilterHotelType ? Hotel.type === currentFilterHotelType : true;

            return matchesSearchTerm && matchesQualification && matchesHotelType;
        });

        // Append filtered Hotels to the Hotel container
        filteredHotels.forEach((Hotel) => {
            // Create the Hotel card element
            const HotelCard = document.createElement('div');
            HotelCard.classList.add('Hotel-card', 'cursor-pointer'); // 'cursor-pointer' to indicate it's clickable
            // HotelCard.onclick = () => window.open(`/hotels?id=${Hotel.id}`, '_blank'); // Open in a new tab
            HotelCard.onclick = () => showHotelModal(Hotel); // Open modal on click
            
            // Create the Hotel image container and set its background image
            const HotelImage = document.createElement('div');
            HotelImage.classList.add('w-full', 'bg-center', 'bg-no-repeat', 'aspect-square', 'bg-cover', 'rounded-xl');
            HotelImage.style.backgroundImage = `url("${Hotel.image}")`;

            // Create the Hotel title element
            const HotelTitle = document.createElement('p');
            HotelTitle.classList.add('text-[#1C160C]', 'text-base', 'font-medium', 'leading-normal');
            HotelTitle.textContent = Hotel.name;

            // Create the Hotel positions element
            const HotelPositions = document.createElement('p');
            HotelPositions.classList.add('text-[#A18249]', 'text-sm', 'font-normal', 'leading-normal');
            HotelPositions.textContent = `${Hotel.room_name}`;

            // Append elements to the Hotel card
            HotelCard.appendChild(HotelImage);
            HotelCard.appendChild(HotelTitle);
            HotelCard.appendChild(HotelPositions);

            // Append the Hotel card to the Hotel container
            HotelContainer.appendChild(HotelCard);
        });

        // Update currentHotelCount
        currentHotelCount += HotelListings.length;

        // Disable the load more button if no more Hotels are available
        if (HotelListings.length < HotelsPerLoad) {
            const loadMoreButton = document.getElementById('loadMoreButton');
            loadMoreButton.disabled = true;
            loadMoreButton.textContent = 'No More Hotels';
        }
    } catch (error) {
        console.error('Error loading Hotel listings:', error);
    }
};

// Initial load of 5 Hotels
loadHotelListings();

// Load more Hotels when the button is clicked
document.getElementById('loadMoreButton').onclick = () => {
    loadHotelListings(); // Load more Hotels
};

// Add event listener for the search input
document.getElementById('Search').addEventListener('input', (event) => {
    const searchTerm = event.target.value;
    loadHotelListings(searchTerm); // Load Hotels based on the search term
});

// Filtering functions
const filterQualification = (qualification) => {
    currentFilterQualification = qualification;
    currentHotelCount = 0; // Reset Hotel count for new search
    loadHotelListings(document.getElementById('Search').value); // Reload Hotels with current search term
};

const filterHotels = (HotelType) => {
    currentFilterHotelType = HotelType;
    currentHotelCount = 0; // Reset Hotel count for new search
    loadHotelListings(document.getElementById('Search').value); // Reload Hotels with current search term
};

const filterHotelsPlace = (HotelType) => {
    currentFilterHotelType = HotelType;
    currentHotelCount = 0; // Reset Hotel count for new search
    loadHotelListings(document.getElementById('Search').value); // Reload Hotels with current search term
};

// Auto-load more Hotels when scrolling down
const handleScroll = () => {
    const scrollableHeight = document.documentElement.scrollHeight; // Total height of the document
    const scrollTop = window.scrollY; // Distance from the top of the viewport
    const clientHeight = window.innerHeight; // Height of the viewport

    // Check if user has scrolled near the bottom of the page
    if (scrollTop + clientHeight >= scrollableHeight - 100) {
        loadHotelListings(); // Load more Hotels
    }
};
// Function to update the UI with the customer's name
function updateUIWithCustomerName(customerName) {
    const loginButton = document.querySelector('.login-button');
    const bookingButton = document.querySelector('.booking-button');

    // Replace the login button with a welcome message
    loginButton.innerHTML = `<span class="truncate">Welcome, ${customerName}</span>`;
    loginButton.classList.remove('login-button'); // Remove the old class
    loginButton.classList.add('welcome-button'); // Add a new class if needed
}

// Function to check login status on page load
function checkLoginStatus() {
    const customerName = localStorage.getItem('customerName');
    const isLoggedIn = localStorage.getItem('isLoggedIn');

    if (isLoggedIn === 'true' && customerName) {
        updateUIWithCustomerName(customerName); // Update UI if logged in
    }
}
checkLoginStatus();
// Add scroll event listener
window.addEventListener('scroll', handleScroll);