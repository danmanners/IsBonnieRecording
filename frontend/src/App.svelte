<script>
  let buttonColor = "black";
  let buttonPressed = { status: false };
  let buttonDefaultText = "Check Status";
  const url = "http://localhost/api/recording";

  async function checkLightStatus() {
    const res = await fetch(url);
    let jsonResponse = await res.json();
    let lightStatus = await jsonResponse.recording;
    if (res.ok) {
      if (lightStatus == true) {
        buttonColor = "purple";
        return "recording";
      }

      if (lightStatus == false) {
        buttonColor = "black";
        return "not recording";
      }
    } else {
      throw new Error(res.text());
    }
  }

  async function updateLightStatus() {
    const res = await fetch(url);
    let jsonResponse = await res.json();
    let lightStatus = await jsonResponse.recording;

    let headers = {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    }

    if (res.ok) {
      if (lightStatus == true) {
        fetch(url, {
          method: "POST",
          headers: headers,
          body: JSON.stringify({
            recording: false,
          }),
        });
        buttonColor = "black";
        return "not recording";
      }

      if (lightStatus == false) {
        fetch(url, {
          method: "POST",
          headers: headers,
          body: JSON.stringify({
            recording: true,
          }),
        });
        buttonColor = "purple";
        return "recording";
      }
    } else {
      throw new Error(res.text());
    }
  }

  let promise = checkLightStatus();

  function handleClick() {
    promise = updateLightStatus();
  }
</script>

<main>
  <nav class="purple lighten-1" role="navigation">
    <div class="nav-wrapper container">
      <a id="logo-container" class="brand-logo center">VOSuperhero</a>
    </div>
  </nav>

  <div class="section no-pad-bot" id="index-banner">
    <div class="container">
      <br /><br />
      <h1 class="header center orange-text">Recording Toggle</h1>
      <div class="row center">
        <h5 class="header col s12 light">
          Simply press the button; it'll change the LED in Dan's office to let
          him know that Bonnie is recording!
        </h5>
      </div>
      <div class="row center">
        <button
          on:click={handleClick}
          class="waves-effect waves-light btn-large {buttonColor}"
        >
          {#if buttonPressed.status}
            {buttonDefaultText}
          {/if}
          {#await promise}
            ...waiting
          {:then recordingStatus}
            {recordingStatus}
          {:catch error}
            {error.message}
          {/await}
        </button>
      </div>
      <br /><br />
    </div>
  </div>
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
