const libStyle = 'background-color: darkblue; color: white; font-style: italic; padding:.2em;'
console.log(`%c =============================================== 
\r --------------- KernelFoodsInc. --------------- 
\r --- utils-lib loaded @ %s --- 
\r ----------------------------------------------- `, libStyle+' font-size: 1em;', (new Date()).toLocaleString())
// const style = 'color: green; font-size: 2em;'
// document.addEventListener("DOMContentLoaded", () => {console.log(`%cdomcontent: ${(new Date)}`, style)})
// window.addEventListener("load", () => {console.log(`%cload: ${(new Date)}`, style)})



async function fetchAll(url1, url2, url3, options = {}) {
    try {
      // Create all fetch promises
      const fetchPromise1 = fetch(url1, options);
      const fetchPromise2 = fetch(url2, options);
      const fetchPromise3 = fetch(url3, options);

      // Wait for all promises to resolve
      const [response1, response2, response3] = await Promise.all([
        fetchPromise1,
        fetchPromise2,
        fetchPromise3
      ]);

      // Check if responses are OK
      if (!response1.ok) {
        throw new Error(
          `Error fetching ${url1}: ${response1.status} ${response1.statusText}`
        );
      }

      if (!response2.ok) {
        throw new Error(
          `Error fetching ${url2}: ${response2.status} ${response2.statusText}`
        );
      }

      if (!response3.ok) {
        throw new Error(
          `Error fetching ${url3}: ${response3.status} ${response3.statusText}`
        );
      }

      // Parse all responses as JSON
      const data1 = await response1.json();
      const data2 = await response2.json();
      const data3 = await response3.json();

      // Return all responses in a single object
      return {
        response1: data1,
        response2: data2,
        response3: data3,
      };
    } catch (error) {
      console.error("Error fetching URLs:", error);
      throw error;
    }
  }