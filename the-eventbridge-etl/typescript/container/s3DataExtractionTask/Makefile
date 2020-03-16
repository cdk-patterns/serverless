# definition of the default target
.DEFAULT_GOAL = image

# shell target is phony (no files to check)
.PHONY = shell

DEFAULT_TAG = local/producer

image:
	docker build -t $(DEFAULT_TAG) .

shell: image
	docker run -it --entrypoint "/bin/bash" $(DEFAULT_TAG)

run: image
	docker run -i $(DEFAULT_TAG)

prune:
	docker system prune --all --force
