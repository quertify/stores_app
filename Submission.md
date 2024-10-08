### Which test did you complete? (backend or full-stack)
**Ans:** Backend

### If you had chosen to spend more time on this test, what would you have done differently?
**Ans:** 
There are a few things which I think I could have added as:
1. **Integrated Swagger UI** to this project so that documentation of the APIs could be more handy.
2. **Added logging and monitoring** to make the application more maintainable and to better handle issues during scaling.
3. **Implemented caching** of store latitude and longitude information to reduce the number of network calls to the external API and improve application speed.
4. **Enhanced security features** for the API, such as rate limiting, to secure the endpoints against misuse.
5. **Adding dedicated config file**  for developer and production environment
6. **Added more tests** for app testing
7. **Added more features like adding new locations of stores**
### What part did you find the hardest? What part are you most proud of? In both cases, why?
**Ans:** 
I found it most challenging that while fetching the coordinates, the API was takeing lot of time to get coordinates one by one. I wanted to make it faster, so I took a design decision to improve it by using the bulk postcode API, which allows fetching up to 100 latitudes and longitudes at once. This approach involved making chunks of the postcode list and fetching data in bulk rather than making multiple single postcode API calls. It took some time to think and reach this conclusion.

I am most proud of reaching this breakthrough and also deciding to paginate the API to fetch locations within a given radius. This ensures that the API is responsive and scalable. Additionally, I am proud of learning about the Haversine function. I had to do some research to calculate the distance between two points, and it was worth it.
reference: https://en.wikipedia.org/wiki/Haversine_formula


### What is one thing we could do to improve this test?
**Ans:** I think there could be more detailed descriptions of the constraints for this problem. Providing clearer constraints would help in defining the scope of the solution and ensure that all potential edge cases are addressed more effectively.
