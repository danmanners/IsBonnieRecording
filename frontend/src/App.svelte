<script>
	export let recording
</script>

<main>
	<nav class="purple lighten-1" role="navigation">
		<div class="nav-wrapper container">
			<a id="logo-container" class="brand-logo center"
				>VOSuperhero</a
			>
		</div>
	</nav>

	<div class="section no-pad-bot" id="index-banner">
		<div class="container">
			<br /><br />
			<h1 class="header center orange-text">Recording Toggle</h1>
			<div class="row center">
				<h5 class="header col s12 light">
					Simply press the button; it'll change the LED in Dan's
					office to let him know that Bonnie is recording!
				</h5>
			</div>
			<div class="row center">
				<button class="waves-effect waves-light btn-large purple" value="Recording">
					Toggle Recording Light
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
