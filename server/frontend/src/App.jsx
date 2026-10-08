import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [dealers, setDealers] = useState([]);
  const [selectedState, setSelectedState] = useState("");
  const [selectedDealer, setSelectedDealer] = useState(null);
  const [reviews, setReviews] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loggedInUser, setLoggedInUser] = useState(null);
  const [loginError, setLoginError] = useState("");

  const [reviewText, setReviewText] = useState("");

  const loadDealers = async (state = "") => {
    setLoading(true);
    setError("");

    try {
      const url = state
        ? `/api/dealers/state/${encodeURIComponent(state)}`
        : "/api/dealers";

      const response = await axios.get(url);
      setDealers(response.data);
    } catch (err) {
      console.error(err);
      setError("Unable to load dealers.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDealers();
  }, []);

  const handleStateChange = (event) => {
    const state = event.target.value;
    setSelectedState(state);
    setSelectedDealer(null);
    loadDealers(state);
  };

  const handleLogin = async (event) => {
    event.preventDefault();
    setLoginError("");

    try {
      const response = await axios.post(
        "/api/login",
        {
          username,
          password,
        },
        {
          withCredentials: true,
        }
      );

      setLoggedInUser(response.data.username);
      setUsername("");
      setPassword("");
    } catch (err) {
      console.error(err);
      setLoginError("Invalid username or password.");
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post(
        "/api/logout",
        {},
        {
          withCredentials: true,
        }
      );

      setLoggedInUser(null);
      setSelectedDealer(null);
      setReviews([]);
      setReviewText("");
    } catch (err) {
      console.error(err);
    }
  };

  const openDealer = async (dealerId) => {
    setError("");

    try {
      const [dealerResponse, reviewResponse] = await Promise.all([
        axios.get(`/api/dealers/${dealerId}`),
        axios.get(`/api/dealers/${dealerId}/reviews`),
      ]);

      setSelectedDealer(dealerResponse.data);
      setReviews(reviewResponse.data);
      setReviewText("");

      window.history.pushState(
        {},
        "",
        `/dealer/${dealerId}`
      );
    } catch (err) {
      console.error(err);
      setError("Unable to load dealer details.");
    }
  };

  const goBack = () => {
    setSelectedDealer(null);
    setReviews([]);
    setReviewText("");

    window.history.pushState({}, "", "/");
    loadDealers(selectedState);
  };

  const handleSubmitReview = async () => {
  if (!reviewText.trim()) {
    alert("Please enter a review.");
    return;
  }

  try {
    await axios.post(
      `/api/dealers/${selectedDealer.id}/reviews/create`,
      {
        review: reviewText,
      },
      {
        withCredentials: true,
      }
    );

    const response = await axios.get(
      `/api/dealers/${selectedDealer.id}/reviews`
    );

    setReviews(response.data);
    setReviewText("");
  } catch (error) {
    console.error(error);
    alert("Unable to submit review.");
  }
};

  return (
    <div
      style={{
        padding: "30px",
        fontFamily: "Arial",
        maxWidth: "1100px",
        margin: "auto",
      }}
    >
      <h1>Dealerships</h1>

      {/* LOGIN */}
      {!selectedDealer && !loggedInUser && (
        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "20px",
            marginBottom: "25px",
          }}
        >
          <h2>Login</h2>

          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              style={{
                padding: "10px",
                marginRight: "10px",
              }}
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{
                padding: "10px",
                marginRight: "10px",
              }}
            />

            <button
              type="submit"
              style={{
                padding: "10px 20px",
              }}
            >
              Login
            </button>
          </form>

          {loginError && <p>{loginError}</p>}
        </div>
      )}

      {/* LOGGED IN USER */}
      {loggedInUser && !selectedDealer && (
        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "15px",
            marginBottom: "25px",
          }}
        >
          <strong>Logged in as: {loggedInUser}</strong>

          <button
            onClick={handleLogout}
            style={{
              marginLeft: "20px",
              padding: "8px 15px",
            }}
          >
            Logout
          </button>
        </div>
      )}

      {/* DEALER DETAILS PAGE */}
      {selectedDealer ? (
        <div>
          <button
            onClick={goBack}
            style={{
              padding: "10px 18px",
              marginBottom: "20px",
            }}
          >
            ← Back to Dealers
          </button>

          <h2>Dealer Details</h2>

          <div
            style={{
              border: "1px solid #ddd",
              borderRadius: "8px",
              padding: "25px",
              marginBottom: "25px",
            }}
          >
            <h2>{selectedDealer.full_name}</h2>

            <p>
              <strong>Dealer ID:</strong> {selectedDealer.id}
            </p>

            <p>
              <strong>City:</strong> {selectedDealer.city}
            </p>

            <p>
              <strong>State:</strong> {selectedDealer.state}
            </p>

            <p>
              <strong>Address:</strong> {selectedDealer.address}
            </p>

            <p>
              <strong>ZIP:</strong> {selectedDealer.zip}
            </p>

            <p>
              <strong>Latitude:</strong> {selectedDealer.lat}
            </p>

            <p>
              <strong>Longitude:</strong> {selectedDealer.lng}
            </p>
          </div>

          {/* REVIEWS */}
          <h2>Reviews</h2>

          {reviews.length === 0 ? (
            <p>No reviews yet.</p>
          ) : (
            reviews.map((review) => (
              <div
                key={review.id}
                style={{
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  padding: "20px",
                  marginBottom: "15px",
                }}
              >
                <p>
                  <strong>User:</strong> {review.username}
                </p>

                <p>
                  <strong>Review:</strong> {review.review}
                </p>

                <p>
                  <strong>Sentiment:</strong>{" "}
                  {review.sentiment || "Not analyzed"}
                </p>
              </div>
            ))
          )}

          {/* POST REVIEW FORM */}
          {loggedInUser && (
            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: "8px",
                padding: "25px",
                marginTop: "25px",
              }}
            >
              <h2>Post a Review</h2>

              <textarea
                placeholder="Enter your review"
                rows="5"
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                style={{
                  width: "100%",
                  padding: "12px",
                  boxSizing: "border-box",
                  marginBottom: "15px",
                }}
              />

             <button
  type="button"
  onClick={handleSubmitReview}
  style={{
    padding: "10px 20px",
  }}
>
  Submit Review
</button>
            </div>
          )}
        </div>
      ) : (
        <>
          {/* STATE FILTER */}
          <div style={{ marginBottom: "25px" }}>
            <label>
              <strong>Filter by State: </strong>

              <select
                value={selectedState}
                onChange={handleStateChange}
                style={{
                  padding: "10px",
                  marginLeft: "10px",
                  minWidth: "180px",
                }}
              >
                <option value="">All States</option>
                <option value="Kansas">Kansas</option>
                <option value="Colorado">Colorado</option>
                <option value="Illinois">Illinois</option>
              </select>
            </label>
          </div>

          <h2>
            {selectedState
              ? `Dealers in ${selectedState}`
              : "Available dealers"}
          </h2>

          {loading && <p>Loading dealers...</p>}

          {error && <p>{error}</p>}

          {!loading &&
            !error &&
            dealers.map((dealer) => (
              <div
                key={dealer.id}
                style={{
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  padding: "20px",
                  marginBottom: "15px",
                }}
              >
                <h2>{dealer.full_name}</h2>

                <p>
                  <strong>City:</strong> {dealer.city}
                </p>

                <p>
                  <strong>State:</strong> {dealer.state}
                </p>

                <p>
                  <strong>Address:</strong> {dealer.address}
                </p>

                <p>
                  <strong>ZIP:</strong> {dealer.zip}
                </p>

                {loggedInUser && (
                  <button
                    onClick={() => openDealer(dealer.id)}
                    style={{
                      padding: "10px 18px",
                      marginTop: "10px",
                    }}
                  >
                    Review Dealer
                  </button>
                )}
              </div>
            ))}
        </>
      )}
    </div>
  );
}

export default App;